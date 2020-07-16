import os
import pathlib
import shutil
import tempfile

from celery.decorators import task
from django.conf import settings

from . import utils


@task(name='packages.fetch_package_from_github')
def fetch_package_from_github(config):
    with tempfile.TemporaryDirectory() as tmpdir:
        mgr = utils.GitHubArtifactManager(config, tmpdir)
        tmp_filepaths = mgr.sync()

        for filepath in tmp_filepaths:
            utils.unzip(filepath)

        tmp_pathlib = pathlib.Path(tmpdir)
        filematcher = '**/*%s*.tar.bz2' % (config['plugin_name'])
        for package in tmp_pathlib.glob(filematcher):
            shutil.copy(package, pathlib.Path('/data') / package.name)
    return config


@task(name='packages.reindex_conda_server')
def reindex_conda_server(config):
    # TODO: run `conda index` on q2hq worker
    return config


@task(name='packages.integrate_new_package')
def integrate_new_package(config):
    # TODO: probably needs to run on a GitHub workflow, for sandboxing
    return config


def handle_new_builds(payload):
    chain = fetch_package_from_github.s(payload) \
        | reindex_conda_server.s() \
        | integrate_new_package.s()
    return chain()
