from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from apps.accounts import loggers
from apps.accounts.validators import validate_username, validate_user_id, validate_email
from apps.core.exceptions import InvalidData, ServiceNotAvailable

UserModel = get_user_model()


def create_user(username: str, first_name: str, password: str, commit: bool = True, **extra_fields):
    """
    Создание новго пользователя.
    :param username: Юзернейм пользователя.
    :param first_name: Имя пользователя.
    :param password: Пароль пользователя.
    :param extra_fields: Остальные поля.
    :return: Новый пользователь.
    :raises ValidationError: Не корректные данные.
    """

    if extra_fields.setdefault("is_superuser", False):
        extra_fields['is_staff'] = True
    password = make_password(password)
    user = UserModel(username=username, first_name=first_name, password=password, **extra_fields)
    user.full_clean()

    if commit:
        try:
            user.save()
            loggers.services.info(
                f'User success created '
                f'[id:{user.id}] '
                f'[username:{username}] '
                f'[is_superuser:{user.is_superuser}] '
                f'[is_staff:{user.is_staff}]'
            )
        except Exception as error:
            loggers.services.error(f'Failed to save user [username:{username}] [error: {error}]')
            raise error

    return user


def get_user_by_id(user_id: str | int) -> UserModel:
    loggers.services.debug(f'Getting user by id [id: {user_id}]')
    return UserModel.objects.get(id=int(user_id))


def get_user_by_username(username: str) -> UserModel:
    loggers.services.debug(f'Getting user by username [username: {username}]')
    return UserModel.objects.get(**{f'{UserModel.USERNAME_FIELD}__iexact': username})


def get_user_by_email(email: str, is_email_verified: bool = True, is_email_primary: bool = True) -> UserModel:
    loggers.services.debug(
        f'Getting user by email '
        f'[email: {email}] '
        f'[is_email_verified:{is_email_verified}] '
        f'[is_email_verified:{is_email_verified}]'
    )
    raise ServiceNotAvailable('Взаимодействия с email не доступно')


def get_user_by_login(login: str | int):
    """
    Поиск пользователя по логину.
    Логином является Username и Id пользователя
    """
    login = str(login).strip()
    loggers.services.debug(f'Getting user by login [login: {login}]')
    try:
        validate_user_id(login)
        return get_user_by_id(login)
    except InvalidData:
        pass
    try:
        validate_username(login)
        return get_user_by_username(username=login)
    except InvalidData:
        pass

    try:
        validate_email(login)
        return get_user_by_email(email=login, is_email_verified=True, is_email_primary=True)
    except InvalidData:
        pass

    raise ValueError()
