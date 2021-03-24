# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pathlib
import shutil
import tempfile
import urllib.error

from celery import chain
from celery.decorators import task
from celery.utils.log import get_task_logger
import conda_build.api
from django import conf

from . import utils
from ..packages.models import Package, PackageBuild
from config.celery import app


logger = get_task_logger(__name__)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # cron job - reindex staging server every tenish minutes
    # TODO: stop hard-coding the release
    staging_path = pathlib.Path(conf.settings.CONDA_ASSET_PATH) / 'qiime2' / '2021.4' / 'staged'

    sender.add_periodic_task(
        600.0,  # seconds
        reindex_conda_server.s(dict(), str(staging_path), '2021.4-staged'),
        name='packages.reindex_staging',
    )


def handle_new_builds(ctx):
    package_id = ctx.pop('package_id')
    run_id = ctx.pop('run_id')
    version = ctx.pop('version')
    package_name = ctx.pop('package_name')
    repository = ctx.pop('repository')
    artifact_name = ctx.pop('artifact_name')
    github_token = ctx.pop('github_token')
    channel = ctx.pop('channel')
    channel_name = ctx.pop('channel_name')

    return chain(
        create_package_build_record_and_update_package.s(
            ctx, package_id, run_id, version, package_name, repository, artifact_name,
        ),

        fetch_package_from_github.s(
            github_token, repository, run_id, channel, package_name, artifact_name,
        ).apply_async(countdown=600),

        reindex_conda_server.s(
            channel, channel_name,
        ),

        package_build_record_unverified_channel_finished.s(),
    ).delay()


@task(name='db.create_package_build_record_and_update_package')
def create_package_build_record_and_update_package(
        ctx, package_id, run_id, version, package_name, repository, artifact_name):
    package_build_record = PackageBuild.objects.create(
        package_id=package_id,
        github_run_id=run_id,
        version=version,
        artifact_name=artifact_name,
    )

    package = Package.objects.get(pk=package_id)
    package.name = package_name
    package.repository = repository
    package.save()

    ctx['package_build_record'] = package_build_record.pk

    return ctx


@task(name='packages.fetch_package_from_github',
      autoretry_for=[urllib.error.HTTPError, urllib.error.URLError, utils.GitHubNotReadyException],
      max_retries=12, retry_backoff=3 * 60, retry_backoff_max=90 * 60)
def fetch_package_from_github(ctx, github_token, repository, run_id, channel, package_name, artifact_name):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_pathlib = pathlib.Path(tmpdir)

        mgr = utils.GitHubArtifactManager(github_token, repository, run_id, artifact_name, tmp_pathlib)
        tmp_filepaths = mgr.sync()

        for filepath in tmp_filepaths:
            utils.unzip(filepath)

        unverified_pkgs_fp = pathlib.Path(channel)
        utils.bootstrap_pkgs_dir(unverified_pkgs_fp)

        filematcher = '**/*%s*.tar.bz2' % (package_name,)
        for from_path in tmp_pathlib.glob(filematcher):
            to_path = unverified_pkgs_fp / from_path.parent.name / from_path.name
            shutil.copy(from_path, to_path)

    return ctx


@task(name='packages.reindex_conda_server')
def reindex_conda_server(ctx, channel, channel_name):
    conda_config = conda_build.api.Config(verbose=False)
    conda_build.api.update_index(
        channel,
        config=conda_config,
        threads=1,
        channel_name=channel_name,
    )

    return ctx


@task(name='db.package_build_record_set_unverified_true')
def package_build_record_unverified_channel_finished(ctx):
    pk = ctx.pop('package_build_record')

    package_build_record = PackageBuild.objects.get(pk=pk)
    package_build_record.unverified = True
    package_build_record.save()

    return ctx
