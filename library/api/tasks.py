from celery.decorators import task
from django.conf import settings

from .utils import GitHubArtifactManager


@task(name='packages.fetch_package_from_github')
def fetch_package_from_github(payload):
    mgr = GitHubArtifactManager(
        settings.GITHUB_TOKEN,
        payload['repository'],
        payload['run_id'],
        settings.CONDA_ASSET_PATH,
    )
    tmp_filepaths = mgr.sync()
    return tmp_filepaths

@task(name='packages.reindex_conda_server')
def reindex_conda_server():
    # TODO: unzip packages
    # TODO: run `conda index` on q2hq worker
    pass


@task(name='packages.integrate_new_package')
def integrate_new_package():
    # TODO: probably needs to run on a GitHub workflow, for sandboxing
    pass


def handle_new_builds(payload):
    chain = fetch_package_from_github.s(payload) \
        | reindex_conda_server.s() \
        | integrate_new_package.s()
    return chain()
