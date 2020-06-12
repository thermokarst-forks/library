from django import forms


class PackageIntegrationForm(forms.Form):
    token = forms.UUIDField(required=True)
    repository = forms.CharField(required=True)
    run_id = forms.CharField(required=True)
