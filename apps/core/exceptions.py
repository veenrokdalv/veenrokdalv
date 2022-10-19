from django.core.exceptions import ValidationError


class ExtendedValidationError(ValidationError):
    code = 'undefined'
    message = 'Error'

    def __init__(self, message=None, code=None, params=None):
        message = message or self.message
        code = code or self.code
        super().__init__(message=message, code=code, params=params)


class InvalidData(ExtendedValidationError):
    code = 'invalid_data'
    message = 'Неверные данные'


class ServiceNotAvailable(ExtendedValidationError):
    code = 'service_not_avaible'
    message = 'Сервис не доступен'