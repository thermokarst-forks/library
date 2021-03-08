# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os

from django import forms, conf

from ..packages.models import Package


class PackageIntegrationForm(forms.Form):
    token = forms.UUIDField(required=True)
    run_id = forms.CharField(required=True)
    version = forms.CharField(required=True)
    package_name = forms.CharField(required=True)
    repository = forms.CharField(required=True)
    artifact_name = forms.CharField(required=True)

    def is_known(self):
        try:
            package = Package.objects.get(token=self.cleaned_data['token'])

            config = {
                'package_id': package.pk,
                'run_id': self.cleaned_data['run_id'],
                'version': self.cleaned_data['version'],
                'package_name': self.cleaned_data['package_name'],
                'repository': self.cleaned_data['repository'],
                'artifact_name': self.cleaned_data['artifact_name'],
                'github_token': conf.settings.GITHUB_TOKEN,
                'channel': os.path.join(conf.settings.CONDA_ASSET_PATH, 'qiime2', 'unverified'),
                'channel_name': 'qiime2/unverified',
            }
        except Package.DoesNotExist:
            config = None

        return config
