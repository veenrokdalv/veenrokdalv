from django.conf import settings

from apps.core.exceptions import InvalidData, ExtendedValidationError


class SignInError(ExtendedValidationError):
    code = 'sign_in_error'
    message = 'Ошибка входа'


class SignUpError(ExtendedValidationError):
    code = 'sign_up_error'
    message = 'Ошибка при регистрации'

class InvalidLogin(InvalidData):
    message = 'Логином является ID аккаунта или Username пользователя.'


class InvalidAccountId(InvalidData):
    message = 'Неверный AccountID. AccountID - целое, положительно число'


class InvalidMinLengthUsername(InvalidData):
    message = f'Username должен быть длиннее, чем {settings.USERNAME_MIN_LENGTH} символов'


class InvalidMaxLengthUsername(InvalidData):
    message = f'Username должен быть короче, чем {settings.USERNAME_MAX_LENGTH} символа'


class InvalidUsernameFirstChar(InvalidData):
    message = f'Username должен начинаться с латинской буквы или _'


class InvalidUsernameAllowedChars(InvalidData):
    message = f'Username может содержать только латинские буквы, цифры и _'


class LoginFailed(InvalidData):
    message = f'Имя должен быть длиннее, чем 1 символ'


class InvalidMaxLengthFirstName(InvalidData):
    message = f'Имя должен быть короче, чем 64 символа'


class InvalidMaxLengthLastName(InvalidData):
    message = f'Фамилия должена быть короче, чем 64 символа'


class InvalidEmail(InvalidData):
    message = f'Некоректный адрес электронной почты.'


class InvalidLoginOrPassword(SignInError):
    message = 'Не верный логин или пароль'


class PasswordNotMatch(SignUpError):
    message = 'Пароли не совпадают'