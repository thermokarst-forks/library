import json
import urllib.request


class GitHubArtifactManager:
    def __init__(self, github_token, github_repository, run_id):
        # TODO: validate inputs
        self.github_token = github_token
        self.github_repository = github_repository
        self.run_id = run_id
        
    def fetch_json_url(self, url):
        # TODO: set token in header
        response = urllib.request.urlopen(url)
        # TODO: check response status code
        data = response.read()
        decoded = data.decode('utf-8')
        return json.loads(decoded)

    def fetch_artifact_records(self):
        url = 'https://github.com/repos/%s/actions/runs/%s/artifacts' \
            % (self.github_repository, self.run_id)
        records = self.fetch_json_url(url)
        # TODO: validate record length/shape/etc
        return records

    def filter_and_validate_artifact_records(self, records):
        # TODO: check file size
        # TODO: check for linux and darwin packages
        return records
    
    def download_artifacts(records):
        fps = []
        for record in records:
            fp = self.fetch_artifact(record)
            fps.append(fp)
        return fps
            
    def sync(self):
        records = self.fetch_artifact_records()
        records = self.filter_and_validate_artifact_records(records)
        local_fps = self.download_artifacts(records)
        # TODO: validate local_fps
        return local_fps
