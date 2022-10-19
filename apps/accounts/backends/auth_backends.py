from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest

from apps.accounts import loggers
from apps.accounts.checks import is_login_valid
from apps.accounts.services import get_user_by_login, get_user_by_username, get_user_by_id, get_user_by_email

__all__ = (
    'UserIdAndPasswordBackend',
    'CIUsernameAndPasswordBackend',
    'CIEmailAndPasswordBackend',
    'LoginAndPasswordBackend',
)

UserModel = get_user_model()


class _BaseUserBackend(ModelBackend):

    def get_user(self, user_id: int | str):
        try:
            user = get_user_by_id(user_id=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None


class UserIdAndPasswordBackend(_BaseUserBackend):

    def authenticate(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        password = kwargs.get('password')

        if user_id is None or password is None:
            loggers.auth_backends.debug(
                f'UserId [user_id:{user_id}] or password not set'
            )
            return None

        try:
            user = get_user_by_id(user_id=user_id)
        except UserModel.DoesNotExist:
            loggers.auth_backends.info(
                f'User failed authenticate by id [id:{user.id}] and password. [error:User not found]'
            )
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                loggers.auth_backends.info(f'User success authenticate by id [id:{user_id}] and password')
                return user
            else:
                loggers.auth_backends.info(
                    f'User failed authenticate by, id [{user.id}] and password. [error:Invalid password]'
                )


class CIUsernameAndPasswordBackend(_BaseUserBackend):
    def authenticate(self, request, **kwargs):
        username = kwargs.get(UserModel.USERNAME_FIELD, None)
        password = kwargs.get('password', None)
        if username is None or password is None:
            loggers.auth_backends.debug(
                f'Username [username:{username}] or password not set'
            )
            return None

        try:
            user = get_user_by_username(username=username)
        except UserModel.DoesNotExist:
            loggers.auth_backends.info(
                f'User failed authenticate by username [username:{username}] and password. [error:User not found]'
            )
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                loggers.auth_backends.info(f'User success authenticate by username [username:{username}] and password')
                return user
            else:
                loggers.auth_backends.info(
                    f'User failed authenticate by username [username:{username}] and password. [error:Invalid password]'
                )


class CIEmailAndPasswordBackend(_BaseUserBackend):

    def authenticate(self, request, **kwargs):
        email = kwargs.get('email', None)
        password = kwargs.get('password', None)

        if email is None or password is None:
            loggers.auth_backends.debug(
                f'Email [email:{email}] or password not set'
            )
            return None

        try:
            user = get_user_by_email(email=email)
        except UserModel.DoesNotExist:
            loggers.auth_backends.info(
                f'User failed authenticate by email [email:{email}] and password. [error:User not found]'
            )
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                loggers.auth_backends.info(f'User success authenticate by email [email:{email}] and password')
                return user
            else:
                loggers.auth_backends.info(
                    f'User failed authenticate by email [email:{email}] and password. [error:Invalid password]'
                )


class LoginAndPasswordBackend(_BaseUserBackend):

    def authenticate(self, request, **kwargs):
        login = kwargs.get('login', None)
        password = kwargs.get('password', None)

        if not is_login_valid(login):
            loggers.auth_backends.debug(
                f'Login [login:{login}] invalid'
            )
            return None

        if login is None or password is None:
            loggers.auth_backends.debug(
                f'Login [login:{login}] or password not set'
            )
            return None

        try:
            user = get_user_by_login(login=login)
        except UserModel.DoesNotExist:
            loggers.auth_backends.info(
                f'User failed authenticate by login [login:{login}] and password. [error:User not found]'
            )
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                loggers.auth_backends.info(f'User success authenticate by login [login:{login}] and password')
                return user
            else:
                loggers.auth_backends.info(
                    f'User failed authenticate by login [login:{login}] and password. [error:Invalid password]'
                )
