import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from apps.accounts import loggers
from apps.accounts.exceptions import InvalidMinLengthUsername, InvalidMaxLengthUsername, InvalidUsernameFirstChar, \
    InvalidUsernameAllowedChars, LoginFailed, InvalidMaxLengthFirstName, InvalidMaxLengthLastName, \
    InvalidEmail, InvalidAccountId
from apps.core.exceptions import InvalidData


def validate_username(username: str) -> str:
    """Валидация username пользователя"""

    errors = []
    if username is None:
        raise InvalidData()

    if len(username) < settings.USERNAME_MIN_LENGTH:
        errors.append(InvalidMinLengthUsername())

    if len(username) > settings.USERNAME_MAX_LENGTH:
        errors.append(InvalidMaxLengthUsername())

    if not re.match(rf'^[{settings.USERNAME_ALLOWED_CHARS_TO_FIRST_CHAR}].*$', username):
        errors.append(InvalidUsernameFirstChar())

    if not re.match(r'^[{username_allowed_chars}]*$'.format(username_allowed_chars=settings.USERNAME_ALLOWED_CHARS),
                    username):
        errors.append(InvalidUsernameAllowedChars())

    if errors:
        raise InvalidData(errors)

    return username


def validate_user_id(user_id: str):
    try:
        user_id = int(user_id)
        if user_id <= 0:
            raise InvalidAccountId()
    except (ValueError, TypeError, InvalidAccountId):
        raise InvalidAccountId()


def validate_email(email: str):
    django_validator = EmailValidator()
    try:
        django_validator(email)
    except ValidationError:
        raise InvalidEmail()


def validator_first_name(first_name: str) -> str:
    """Валидация имени пользователя"""
    errors = []

    if first_name is None:
        raise InvalidData()

    if len(first_name) < 1:
        errors.append(LoginFailed())

    if len(first_name) > 64:
        errors.append(InvalidMaxLengthFirstName())

    if errors:
        raise InvalidData(errors)

    return first_name


def validator_last_name(last_name: str) -> str:
    """Валидация фамилии пользователя"""
    errors = []
    if last_name is None:
        return last_name

    if len(last_name) > 64:
        errors.append(InvalidMaxLengthLastName())

    if errors:
        raise InvalidData(errors)

    return last_name
