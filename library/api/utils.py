import json
import os
import shutil
import urllib.request


class GitHubArtifactManager:
    def __init__(self, github_token, github_repository, run_id):
        # TODO: validate inputs
        self.github_token = github_token
        self.github_repository = github_repository
        self.run_id = run_id
        self.base_url = 'https://api.github.com'
        self.root_path = './data'

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

    def fetch_binary_file(self, url, download_path):
        request = self.build_request(url)
        with urllib.request.urlopen(request) as resp, \
                open(download_path, 'wb') as save_fh:
            shutil.copyfileobj(resp, save_fh)

    def fetch_artifact(self, record):
        download_path = os.path.join(self.root_path, record['name'])
        self.fetch_binary_file(record['archive_download_url'], download_path)
        return download_path

    def fetch_artifact_records(self):
        url = '%s/repos/%s/actions/runs/%s/artifacts' \
            % (self.base_url, self.github_repository, self.run_id)
        records = self.fetch_json_data(url)
        return records

    def filter_and_validate_artifact_records(self, records):
        # TODO: check file size
        # TODO: check for linux and darwin packages
        return records

    def download_artifacts(self, records):
        for record in records:
            filepath = self.fetch_artifact(record)
            yield filepath

    def validate_local_filepaths(self, filepaths):
        return filepaths

    def sync(self):
        records = self.fetch_artifact_records()
        filtered_records = self.filter_and_validate_artifact_records(records)
        local_filepaths = self.download_artifacts(filtered_records)
        validated_filepaths = self.validate_local_filepaths(local_filepaths)
        return validated_filepaths
