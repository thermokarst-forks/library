from celery.decorators import task
from celery.utils.log import get_task_logger
from django.conf import settings


from .utils import GitHubArtifactManager


logger = get_task_logger(__name__)


@task(name='packages.fetch_package_from_github')
def fetch_package_from_github(payload):
    logger.info('Debug: %r' % (payload, ))

    # TODO: add settings key to root config
    github_token = settings.get('GITHUB_TOKEN')
    github_repository = payload['repository']
    run_id = payload['run_id']

    mgr = GitHubArtifactManager(github_token, github_repository, run_id)
    tmp_filepaths = mgr.sync()
    return tmp_filepaths


@task(name='packages.reindex_conda_server')
def reindex_conda_server():
    # TODO: run `conda index` on q2hq worker
    pass


@task(name='packages.integrate_new_package')
def integrate_new_package():
    # TODO: probably needs to run on a GitHub workflow, for sandboxing
    pass


# TODO: add some kind of celery workflow to stitch the tasks above together