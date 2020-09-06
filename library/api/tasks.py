import pathlib
import shutil
import tempfile

from celery import chain
from celery.decorators import task
from celery.utils.log import get_task_logger
import conda_build.api

from . import utils
from ..packages.models import Package, PackageBuild


logger = get_task_logger(__name__)


def handle_new_builds(ctx):
    package_id = ctx.pop('package_id')
    run_id = ctx.pop('run_id')
    version = ctx.pop('version')
    package_name = ctx.pop('package_name')
    repository = ctx.pop('repository')
    github_token = ctx.pop('github_token')
    channel = ctx.pop('channel')
    channel_name = ctx.pop('channel_name')

    return chain(
       create_package_build_record_and_update_package.s(
           ctx, package_id, run_id, version, package_name, repository
       ),

       fetch_package_from_github.s(
           github_token, repository, run_id, channel, package_name,
       ),

       reindex_conda_server.s(
           channel, channel_name,
       ),

       package_build_record_unverified_channel_finished.s(),

       integrate_new_package.s(),
    ).delay()


@task(name='db.create_package_build_record_and_update_package')
def create_package_build_record_and_update_package(
        ctx, package_id, run_id, version, package_name, repository):
    package_build_record = PackageBuild.objects.create(
        package_id=package_id,
        github_run_id=run_id,
        version=version,
    )

    package = Package.objects.get(pk=package_id)
    package.name = package_name
    package.repository = repository
    package.save()

    ctx['package_build_record'] = package_build_record.pk

    return ctx


@task(name='packages.fetch_package_from_github')
def fetch_package_from_github(ctx, github_token, repository, run_id, channel, package_name):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_pathlib = pathlib.Path(tmpdir)

        mgr = utils.GitHubArtifactManager(github_token, repository, run_id, tmp_pathlib)
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


@task(name='packages.integrate_new_package')
def integrate_new_package(ctx):
    # TODO: probably needs to run on a GitHub workflow, for sandboxing
    return ctx
