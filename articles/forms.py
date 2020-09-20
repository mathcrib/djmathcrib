from django import forms
from django.core.exceptions import ValidationError

from .models import Article


class AuthorUpdateForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'text', 'parent')

    def clean_parent(self):
        data = self.cleaned_data['parent']
        if not data:
            raise ValidationError('Выберете раздел!')
        return data


class PersonalUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'text', 'parent', 'is_published')
