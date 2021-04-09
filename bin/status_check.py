import json
import sys

import conda.cli.python_api as conda
from ghapi.all import GhApi


ORG = 'qiime2'
BRANCH = 'master'


def latest_commit(package, api):
    resp = api.repos.get_branch(owner=ORG, repo=package, branch=BRANCH)
    return (resp.commit.html_url, resp.commit.sha)


def latest_action_run(package, api, latest_commit_sha):
    resp = api.actions.list_workflow_runs_for_repo(
        owner=ORG, repo=package, branch=BRANCH, event='push',
        per_page=1, page=1)
    run = resp.workflow_runs[0]

    if run.head_branch != BRANCH:
        raise ValueError('run branch %s != master' % (run.head_branch,))

    if run.head_sha != latest_commit_sha:
        raise ValueError('run sha %s != latest commit %s' %
                         (run.head_sha, latest_commit_sha))

    return (run.html_url, run.conclusion, run.status)


def sync_gh(package, api):
    commit_url, commit_ref = latest_commit(package, api)
    action_url, action_conclusion, action_status = latest_action_run(
        package, api, commit_ref)
    return (commit_url, action_url, action_conclusion, action_status)


def library_status(package, epoch):
    resp, _, _ = conda.run_command(
        conda.Commands.SEARCH,
        '-c',
        'https://packages.qiime2.org/qiime2/latest/%s/' % (epoch,),
        package,
        '--json')
    results = json.loads(resp)

    return [build['version'] for build in results[package]][-1]


def format_record(package, gh, test, stage):
    print(package)
    commit_url, action_url, action_conclusion, action_status = gh
    print(commit_url)
    print(action_url)
    print(action_conclusion, action_status)
    print('tested:', test)
    print('staged:', stage)
    print('\n')


def read_packages(fp):
    with open(fp) as fh:
        return [p.strip() for p in fh.readlines()]


if __name__ == '__main__':
    token = sys.argv[1]
    api = GhApi(token=token)

    packages_fp = sys.argv[2]
    packages = read_packages(packages_fp)

    for package in packages:
        github_status = sync_gh(package, api)
        tested_status = library_status(package, 'tested')
        staged_status = library_status(package, 'staged')
        format_record(package, github_status, tested_status, staged_status)
