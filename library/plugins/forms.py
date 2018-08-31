from django import forms

from .models import Plugin, PluginAuthorship


_description_initial = '''# New Plugin Description

> A few things to consider adding here:

* Include a brief summary or the plugin and what it does
* Is there a corresponding publication? Maybe throw a link or two in here.
* Are there docs published somewhere? If so, put a link in! If not, consider publishing those here!
* How should users go about getting help? Should they post to the forum?
  * Consider asking the moderators if they can set up a new tag or category on the forum for you to handle support in.
'''

_install_initial = '''# Directions
1. Install QIIME 2:
        wget ...

2. Run the following:
        conda install ...
'''


# TODO: 'dependencies'
class PluginForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'id': 'description', 'class': 'textarea'}),
                                  initial=_description_initial,
                                  help_text=Plugin._meta.get_field('description').help_text)
    install_guide = forms.CharField(widget=forms.Textarea(attrs={'id': 'install-guide', 'class': 'textarea'}),
                                    initial=_install_initial,
                                    help_text=Plugin._meta.get_field('install_guide').help_text)

    def is_valid(self):
        is_valid = super().is_valid()
        for field in self.errors:
            # Gross, but if there is an error, better mark it as such with CSS
            class_ = self.fields[field].widget.attrs.get('class', '')
            self.fields[field].widget.attrs.update({'class':  ' '.join([class_, 'is-danger'])})
        return is_valid

    class Meta:
        model = Plugin
        fields = ['name', 'title', 'version', 'source_url', 'published', 'short_summary', 'description',
                  'install_guide']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'e.g. my_plugin'}),
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'e.g. q2-my-plugin'}),
            'version': forms.TextInput(attrs={'class': 'input', 'placeholder': 'e.g. 0.2.1'}),
            'source_url': forms.URLInput(attrs={'class': 'input',
                                                'placeholder': 'e.g. https://example.com/q2-my-plugin.git'}),
            'short_summary': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'e.g. All about my plugin!'}),
        }


class PluginAuthorshipForm(forms.ModelForm):
    class Meta:
        model = PluginAuthorship
        fields = ['plugin', 'author', 'list_position']
        widgets = {
            'list_position': forms.NumberInput(attrs={'class': 'input'}),
        }


PluginAuthorshipFormSet = forms.inlineformset_factory(
        Plugin, PluginAuthorship, form=PluginAuthorshipForm, extra=2,
        fk_name='plugin')
