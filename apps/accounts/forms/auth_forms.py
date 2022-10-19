from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.http import HttpRequest

from apps.accounts import loggers
from apps.accounts.exceptions import InvalidLoginOrPassword, PasswordNotMatch
from apps.accounts.services import create_user

UserModel = get_user_model()


class SignInByLoginForm(forms.Form):
    login = forms.CharField(
        label='Логин',
        required=False,
    )

    password = forms.CharField(
        label='Пароль',
        required=False,
        widget=forms.PasswordInput()
    )

    class Meta:
        fields = ('login', 'password')

    def __init__(self, request: HttpRequest, **kwargs):
        self._request = request
        self._user_authenticated = None
        super().__init__(**kwargs)

    def get_user_authenticated(self):
        return self._user_authenticated

    def clean(self):
        loggers.auth_forms.debug(f'Login form [data: {self.cleaned_data}]')
        login = self.cleaned_data['login']
        password = self.cleaned_data['password']
        self._user_authenticated = authenticate(self._request, login=login, password=password)

        if not self._user_authenticated:
            raise InvalidLoginOrPassword()

        return self.cleaned_data


class SignUpForm(forms.ModelForm):

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput()
    )

    password_confirm = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = UserModel
        fields = (
            'username',
            'first_name',
            'last_name',
            'password',
            'password_confirm'
        )

    def clean(self):
        loggers.auth_forms.debug(f'Sign up form [data: {self.cleaned_data}]')
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data.pop('password_confirm')

        if password != password_confirm:
            raise PasswordNotMatch()

        return self.cleaned_data

    def save(self, commit=True):
        create_user(**self.cleaned_data)
