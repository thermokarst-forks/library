# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import datetime
import pathlib
import shutil
import tempfile
import urllib.error

from celery import chain
from celery.decorators import task
from celery.schedules import crontab
from celery.utils.log import get_task_logger
import conda_build.api
from django import conf
from django.db import transaction
from django.utils import timezone
from django_celery_results.models import TaskResult

from . import utils
from . import forms
from ..packages.models import Package, PackageBuild
from config.celery import app


logger = get_task_logger(__name__)

TIME = {
    '03_MIN': 60 * 3,
    '05_MIN': 60 * 5,
    '10_MIN': 60 * 10,
    '90_MIN': 60 * 90,
    '02_HR': 60 * 60 * 2,
}


# For development purposes it's a lot nicer to have short cycle times (30 sec)
if conf.settings.DEBUG:
    TIME = {k: 30 for k in TIME.keys()}


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=4),  # daily at 4a
        celery_backend_cleanup.s(),
        name='db.clean_up_reindex_tasks'
    )

    for gate in ['tested', 'staged']:
        path = forms.BASE_PATH / gate
        sender.add_periodic_task(
            TIME['05_MIN'],
            reindex_conda_server.s(dict(), str(path), '%s-%s' % (conf.settings.QIIME2_RELEASE, gate)),
            name='packages.reindex_%s' % (gate,),
        )


@task(name='db.celery_backend_cleanup')
def celery_backend_cleanup():
    with transaction.atomic():
        TaskResult.objects.filter(
            date_done__lt=timezone.now() - datetime.timedelta(seconds=conf.settings.CELERY_RESULT_EXPIRES),
            task_name__in=[
                'packages.reindex_conda_server',
                'packages.celery_backend_cleanup',
            ],
        ).delete()


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
        ),

        reindex_conda_server.s(
            channel, channel_name,
        ),

        package_build_record_set_unverified_true.s(),

        update_conda_build_config.s(
            github_token, 'main', conf.settings.QIIME2_RELEASE, 'tested', package_name, version),

        # open_pull_request.s(
        #     '%s-%s' % (package_name, version), conf.settings.QIIME2_RELEASE, 'staged', 'main'),

    ).apply_async(countdown=TIME['10_MIN'])


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
      max_retries=12, retry_backoff=TIME['03_MIN'], retry_backoff_max=TIME['90_MIN'])
def fetch_package_from_github(ctx, github_token, repository, run_id, channel, package_name, artifact_name):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_pathlib = pathlib.Path(tmpdir)

        mgr = utils.GitHubArtifactManager(github_token, repository, run_id, artifact_name, tmp_pathlib)
        tmp_filepaths = mgr.sync()

        for filepath in tmp_filepaths:
            utils.unzip(filepath)

        tested_pkgs_fp = pathlib.Path(channel)
        utils.bootstrap_pkgs_dir(tested_pkgs_fp)

        filematcher = '**/*%s*.tar.bz2' % (package_name,)
        for from_path in tmp_pathlib.glob(filematcher):
            to_path = tested_pkgs_fp / from_path.parent.name / from_path.name
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
def package_build_record_set_unverified_true(ctx):
    pk = ctx.pop('package_build_record')

    package_build_record = PackageBuild.objects.get(pk=pk)
    package_build_record.unverified = True
    package_build_record.save()

    # needs to be JSON serializable, sets aren't roundtrippable though, so listify queryset
    ctx['build_artifacts'] = list(PackageBuild.objects.filter(
        package=package_build_record.package,
        version=package_build_record.version,
    ).distinct().values_list('artifact_name', flat=True))

    return ctx


@task(name='git.update_conda_build_config',
      autoretry_for=[utils.AdvisoryLockNotReadyException],
      max_retries=12, retry_backoff=TIME['03_MIN'], retry_backoff_max=TIME['02_HR'])
def update_conda_build_config(ctx, github_token, branch, release, gate, package_name, version):
    # TODO: drop this when alpha2 is ready
    if not ctx['dev_mode']:
        return ctx

    if set(ctx['build_artifacts']) != {'osx-64', 'linux-64'}:
        return ctx

    mgr = utils.CondaBuildConfigManager(github_token, branch, release, gate, package_name, version)
    mgr.update()

    return ctx


# @task(name='git.open_pull_request')
# def open_pull_request(ctx, branch, release, gate, base):
#     # TODO: drop this when alpha2 is ready
#     if not ctx['dev_mode']:
#         return ctx
#
#     if ctx['build_artifacts'] != ('osx-64', 'linux-64'):
#         return ctx
#
#     utils.update_conda_build_config(branch, release, gate)
