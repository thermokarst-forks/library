# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import base64
import contextlib
import json
from packaging import version
import shutil
import urllib.request
import urllib.error
import zipfile

from django.db import connection
from fastcore.utils import HTTP404NotFoundError
from ghapi.all import GhApi
import yaml


class GitHubNotReadyException(Exception):
    pass


class AdvisoryLockNotReadyException(Exception):
    pass


class GitHubArtifactManager:
    def __init__(self, github_token, repository, run_id, artifact_name, tmpdir):
        self.github_token = github_token
        self.github_repository = repository
        self.run_id = run_id
        self.artifact_name = artifact_name
        self.root_pathlib = tmpdir
        self.base_url = 'https://api.github.com'
        self.valid_names = {'linux-64', 'osx-64'}

        self.validate_config()

    def validate_config(self):
        if self.github_token == '':
            raise Exception('TODO1')

        if self.github_repository == '':
            raise Exception('TODO2')
        parts = self.github_repository.split('/')
        if len(parts) != 2:
            raise Exception('TODO3')
        org, repo = parts
        if org == '':
            raise Exception('TODO4')
        if repo == '':
            raise Exception('TODO5')

        if self.run_id == '':
            raise Exception('TODO6')

        if self.artifact_name == '':
            raise Exception('TODO7')

        if self.artifact_name not in self.valid_names:
            raise Exception('TODO8')

    def build_request(self, url, headers=None):
        request = urllib.request.Request(url)
        request.add_header('authorization',
                           'Bearer %s' % (self.github_token, ))
        if headers is not None:
            for k, v in headers.items():
                request.add_header(k, v)
        return request

    def fetch_json_data(self, url):
        headers = {'content-type': 'application/json'}
        request = self.build_request(url, headers)
        response = urllib.request.urlopen(request)
        data = response.read()
        decoded = data.decode('utf-8')
        return json.loads(decoded)

    def fetch_binary_file(self, url, download_pathlib):
        if download_pathlib.exists():
            raise Exception('TODO9')

        try:
            request = self.build_request(url)
            with urllib.request.urlopen(request) as resp, \
                    download_pathlib.open('wb') as save_fh:
                shutil.copyfileobj(resp, save_fh)
        except Exception:
            raise urllib.error.HTTPError

    def fetch_artifact(self, record):
        download_path = self.root_pathlib / record['name']
        self.fetch_binary_file(record['archive_download_url'], download_path)
        return download_path

    def fetch_artifact_records(self):
        url = '%s/repos/%s/actions/runs/%s/artifacts' \
            % (self.base_url, self.github_repository, self.run_id)
        records = self.fetch_json_data(url)
        return records

    def filter_and_validate_artifact_records(self, records):
        filtered_records = list()
        for record in records['artifacts']:
            if record['name'] == self.artifact_name:
                if record['size_in_bytes'] <= 100000000:
                    filtered_records.append(record)
                else:
                    raise Exception('TODO10')

        if len(filtered_records) != 1:
            raise GitHubNotReadyException('TODO11: %r' % (filtered_records, ))

        return filtered_records

    def download_artifacts(self, records):
        return [self.fetch_artifact(record) for record in records]

    def validate_local_filepaths(self, filepaths):
        # TODO: implement this
        return filepaths

    def sync(self):
        records = self.fetch_artifact_records()
        filtered_records = self.filter_and_validate_artifact_records(records)
        local_filepaths = self.download_artifacts(filtered_records)
        validated_filepaths = self.validate_local_filepaths(local_filepaths)
        return validated_filepaths


def unzip(fp_pathlib):
    new_name = '%s_unzipped' % fp_pathlib.name
    with zipfile.ZipFile(fp_pathlib, 'r') as zip_fh:
        zip_fh.extractall(str(fp_pathlib.parent / new_name))


def bootstrap_pkgs_dir(fp_pathlib):
    for arch in ('linux-64', 'osx-64'):
        (fp_pathlib / arch).mkdir(parents=True, exist_ok=True)


@contextlib.contextmanager
def advisory_lock(lock_id):
    lock_id = int(lock_id)
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT pg_try_advisory_lock(%s);', (lock_id,))
        acquired = cursor.fetchall()[0][0]
        yield acquired
    finally:
        cursor.execute('SELECT pg_advisory_unlock(%s);', (lock_id,))
        cursor.close()


class CondaBuildConfigManager:
    def __init__(self, github_token, branch, epoch, gate, package_versions):
        self.github_token = github_token
        self.branch = branch
        self.epoch = epoch
        self.gate = gate
        self.package_versions = {p.replace('-', '_'): v for p, v in package_versions.items()}

        self.validate_config()

        self.path = '%s/%s/conda_build_config.yaml' % (self.epoch, self.gate)

        cmt_msg = 'updating %s %s packages\n\n' % (self.epoch, self.gate)
        for pkg, ver in self.package_versions.items():
            cmt_msg += '- %s=%s\n' % (pkg, ver)
        self.commit_msg = cmt_msg
        # TODO: conditional setup
        self.owner = 'thermokarst'
        self.repo = 'package-integration'
        self.ghapi = None
        self.main_branch = 'main'

    def validate_config(self):
        if self.github_token == '':
            raise Exception('TODO12')

        if self.branch == '':
            raise Exception('TODO13')

        if self.epoch == '':
            raise Exception('TODO14')

        if self.gate not in ('tested', 'staged'):
            raise Exception('TODO15')

        if len(self.package_versions) < 1:
            raise Exception('TODO16')

    def update(self):
        with advisory_lock(42) as lock:
            if lock:
                # Wait until we get a lock before setting up ghapi
                self.ghapi = GhApi(token=self.github_token)
                cbc, sha = self.fetch_from_github()
                for package_name, version in self.package_versions.items():
                    if package_name in cbc:
                        last_versions = cbc[package_name]
                        if len(last_versions) != 1:
                            raise Exception('TODO17')
                        if compare_package_versions(version, last_versions[0]):
                            raise Exception('TODO18')
                    cbc[package_name] = [version]
                self.add_branch_if_missing()
                self.commit_to_github(cbc, sha)
            else:
                raise AdvisoryLockNotReadyException

    def fetch_from_github(self):
        try:
            payload = self.ghapi.repos.get_content(
                owner=self.owner,
                repo=self.repo,
                path=self.path,
                # always use latest main as a basis
                ref=self.main_branch,
            )

            cbc = base64.b64decode(payload['content'])
            parsed = yaml.load(cbc, Loader=yaml.FullLoader)

            results = (parsed, payload['sha'])
        except HTTP404NotFoundError:
            results = (dict(), None)

        return results

    def add_branch_if_missing(self):
        try:
            self.ghapi.repos.get_branch(
                owner=self.owner,
                repo=self.repo,
                branch=self.branch,
            )
        except HTTP404NotFoundError:
            payload = self.ghapi.git.get_ref(
                owner=self.owner,
                repo=self.repo,
                ref='heads/%s' % (self.main_branch,),
            )
            self.ghapi.git.create_ref(
                owner=self.owner,
                repo=self.repo,
                ref='refs/heads/%s' % (self.branch,),
                sha=payload['object']['sha'],
            )


    def commit_to_github(self, cbc, sha):
        updated = yaml.dump(cbc)
        content = base64.b64encode(updated.encode('utf-8')).decode('utf-8')

        self.ghapi.repos.create_or_update_file_contents(
            owner=self.owner,
            repo=self.repo,
            path=self.path,
            message=self.commit_msg,
            content=content,
            sha=sha,
            branch=self.branch
        )

    def open_pr(self):
        self.update()

        payload = self.ghapi.pulls.create(
            owner=self.owner,
            repo=self.repo,
            title=self.commit_msg,
            head=self.branch,
            base=self.main_branch,
            maintainer_can_modify=True,
            draft=False,
        )

        return payload['html_url']


def compare_package_versions(a, b):
    a = version.parse(str(a))
    b = version.parse(str(b))
    return a < b
