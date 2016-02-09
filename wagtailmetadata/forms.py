from django import forms

from .models import SiteMetadataPreferences


class SiteMetadataPreferencesForm(forms.ModelForm):

    class Meta:
        model = SiteMetadataPreferences
        exclude = ('site', )
