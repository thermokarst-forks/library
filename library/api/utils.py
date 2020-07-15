import json
import os
import shutil
import urllib.request


class GitHubArtifactManager:
    def __init__(self, github_token, github_repository, run_id, root_path):
        self.github_token = github_token
        self.github_repository = github_repository
        self.run_id = run_id
        self.root_path = root_path

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

        if self.root_path == '':
            raise Exception('TODO7')
        if not os.path.exists(self.root_path):
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

    def fetch_binary_file(self, url, download_path):
        if os.path.exists(download_path):
            raise Exception('TODO9')

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
        filtered_records, names = list(), set()
        for record in records['artifacts']:
            names.add(record['name'])
            if record['name'] in self.valid_names:
                if record['size_in_bytes'] <= 100000000:
                    filtered_records.append(record)
                else:
                    raise Exception('TODO10')
        if not names >= self.valid_names:
            raise Exception('TODO11')

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
