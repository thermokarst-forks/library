from django import forms

from .models import Plugin, PluginAuthorship


_description_initial = '''# New Plugin Description

> A few things to consider adding here:

* Include a brief summary of the plugin and what it does.
* Is there a corresponding publication? Maybe throw a link or two in here.
* Are there docs published somewhere? If so, put a link in! If not, consider publishing those here!
* How should users go about getting help? Should they post to the QIIME 2 Forum?
  * Consider asking the moderators if they can set up a new tag or category on the forum for you to handle support in.
'''

_install_initial = '''# Directions
Run the following:
```bash
conda install -c my_conda_channel q2-my-plugin
```
'''


class PluginForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'id': 'description', 'class': 'textarea'}),
                                  initial=_description_initial,
                                  help_text=Plugin._meta.get_field('description').help_text)
    install_guide = forms.CharField(widget=forms.Textarea(attrs={'id': 'install-guide', 'class': 'textarea'}),
                                    initial=_install_initial,
                                    help_text=Plugin._meta.get_field('install_guide').help_text)

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['dependencies'] = forms.ModelMultipleChoiceField(
            required=False,
            queryset=Plugin.objects.all(current_user),
            help_text=Plugin._meta.get_field('dependencies').help_text)

    def is_valid(self):
        is_valid = super().is_valid()
        for field in self.errors:
            # Gross, but if there is an error, better mark it as such with CSS
            class_ = self.fields[field].widget.attrs.get('class', '')
            self.fields[field].widget.attrs.update({'class':  ' '.join([class_, 'is-danger'])})
        return is_valid

    class Meta:
        model = Plugin
        fields = ['title', 'version', 'source_url', 'published', 'short_summary', 'description',
                  'install_guide', 'dependencies']
        widgets = {
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


class PluginAuthorshipFormSet(forms.inlineformset_factory(
        Plugin, PluginAuthorship,
        extra=1,
        form=PluginAuthorshipForm,
        fk_name='plugin')):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    # Overriding the clean() to add our custom validation.
    def clean(self):
        user_not_in_author_list = True
        for form in self.forms:
            if self.user == form.cleaned_data.get('author'):
                user_not_in_author_list = False
        if user_not_in_author_list:
            raise forms.ValidationError('You must enter yourself as an author. '
                                        'Save the plugin to add additional authors.', code='author_error1')
        return
