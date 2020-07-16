from django import forms


class PackageIntegrationForm(forms.Form):
    qiime2_plugin_token = forms.UUIDField(required=True)
    repository = forms.CharField(required=True)
    run_id = forms.CharField(required=True)
    plugin_name = forms.CharField(required=True)
