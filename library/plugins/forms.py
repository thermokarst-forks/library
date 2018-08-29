from django.forms import ModelForm

from .models import Plugin


class PluginForm(ModelForm):
    class Meta:
        model = Plugin
        fields = ['name']
