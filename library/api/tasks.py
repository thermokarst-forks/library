import os
import pathlib
import shutil
import tempfile

from celery.decorators import task
import conda_build.api
from django.conf import settings

from . import utils


UNVERIFIED_PKGS_FP = pathlib.Path('/data/unverified')


@task(name='packages.fetch_package_from_github')
def fetch_package_from_github(config):
    with tempfile.TemporaryDirectory() as tmpdir:
        mgr = utils.GitHubArtifactManager(config, tmpdir)
        tmp_filepaths = mgr.sync()

        for filepath in tmp_filepaths:
            utils.unzip(filepath)

        utils.bootstrap_pkgs_dir(UNVERIFIED_PKGS_FP)

        tmp_pathlib = pathlib.Path(tmpdir)
        filematcher = '**/*%s*.tar.bz2' % (config['plugin_name'])
        for package in tmp_pathlib.glob(filematcher):
            shutil.copy(package, UNVERIFIED_PKGS_FP / package.parent.name / package.name)
    return config


@task(name='packages.reindex_conda_server')
def reindex_conda_server(config):
    cfg = conda_build.api.Config(verbose=False)
    conda_build.api.update_index(str(UNVERIFIED_PKGS_FP), config=cfg, threads=1)
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
