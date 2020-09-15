from django import forms

from .models import Article


class AuthorUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'text', 'parent')


class PersonalUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'text', 'parent', 'is_published')
