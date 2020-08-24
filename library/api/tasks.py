import pathlib
import shutil
import tempfile

from celery.decorators import task
import conda_build.api
from django.conf import settings

from . import utils


UNVERIFIED_PKGS_FP = pathlib.Path(settings.CONDA_ASSET_PATH) / 'qiime2-unverified'


@task(name='packages.fetch_package_from_github')
def fetch_package_from_github(config):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_pathlib = pathlib.Path(tmpdir)

        mgr = utils.GitHubArtifactManager(config, tmp_pathlib)
        tmp_filepaths = mgr.sync()

        for filepath in tmp_filepaths:
            utils.unzip(filepath)

        utils.bootstrap_pkgs_dir(UNVERIFIED_PKGS_FP)

        filematcher = '**/*%s*.tar.bz2' % (config['package_name'])
        for from_path in tmp_pathlib.glob(filematcher):
            to_path = UNVERIFIED_PKGS_FP / from_path.parent.name / from_path.name
            shutil.copy(from_path, to_path)

    config['channel'] = str(UNVERIFIED_PKGS_FP)
    return config


@task(name='packages.reindex_conda_server')
def reindex_conda_server(config):
    conda_config = conda_build.api.Config(verbose=False)
    conda_build.api.update_index(
        config['channel'], config=conda_config, threads=1)
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
