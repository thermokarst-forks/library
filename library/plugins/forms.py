from django import forms

from .models import Plugin


class PluginForm(forms.ModelForm):
    def is_valid(self):
        is_valid = super().is_valid()
        for field in self.errors:
            # Gross, but if there is an error, better mark it as such with CSS
            class_ = self.fields[field].widget.attrs.get('class', '')
            self.fields[field].widget.attrs.update({'class':  ' '.join([class_, 'is-danger'])})
        return is_valid

    class Meta:
        model = Plugin
        fields = ['name', 'title', 'version', 'source_url', 'published', 'short_summary', 'install_guide',
                  'description']
        # TODO: , 'authors', 'dependencies'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'e.g. my_plugin'}),
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'e.g. q2-my-plugin'}),
            'version': forms.TextInput(attrs={'class': 'input', 'placeholder': 'e.g. 0.2.1'}),
            'source_url': forms.URLInput(attrs={'class': 'input',
                                                'placeholder': 'e.g. https://example.com/q2-my-plugin.git'}),
            'short_summary': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'e.g. 0.2.1'}),
        }
