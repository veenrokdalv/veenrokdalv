from django import forms

from apps.shorter.models import LinkAlias
from apps.shorter.services import create_link_alias


class CreateLinkAliasForm(forms.ModelForm):

    class Meta:
        model = LinkAlias
        fields = [
            'url',
            'alias',
        ]

    def save(self, commit=True):
        return create_link_alias(**self.cleaned_data)
