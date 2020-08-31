from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            message=_('Пользователь с таким email уже существует!'),
            params={'value': value},
        )


class CreationForm(UserCreationForm):
    invite_key = forms.CharField(widget=forms.HiddenInput())
    email = forms.EmailField(validators=[validate_email])

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'invite_key')
