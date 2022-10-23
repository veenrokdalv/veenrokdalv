import typing
from getpass import getpass

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand


class ValueDefaultUnSet:
    pass


class ExtendedBaseCommand(BaseCommand):

    def _pre_input_render(self, message):
        self.stdout.write('_' * 20)
        self.stdout.write(message, ending='')

    def render_input_error(self, error: ValidationError | typing.Any):
        if isinstance(error, ValidationError):
            error_message = '\n'.join(error.messages)
            self.stderr.write(self.style.ERROR(error_message))
        else:
            self.stderr.write(repr(error))

    def _post_input_render(self):
        self.stdout.write('=' * 20)

    def validate_value(self, value, validators, render_errors: bool = True) -> bool:
        is_valid = True
        for validator in validators:
            try:
                if hasattr(validator, 'validate'):
                    validator.validate(value)
                elif callable(validator):
                    validator(value)
                else:
                    raise TypeError
            except Exception as error:
                if render_errors:
                    self.render_input_error(error=error)
                is_valid = False
        return is_valid

    def input(self,
              prompt: str,
              message: str = '',
              validators: typing.Iterable[typing.Callable] = (),
              default=ValueDefaultUnSet(),
              cast=str,
              echo_turned_on: bool = True) -> str:

        while True:
            self._pre_input_render(message=message)
            if isinstance(default, ValueDefaultUnSet):
                input_prompts_message = f'{prompt}: '

            elif not echo_turned_on:
                input_prompts_message = f'{prompt} (По-умолчанию: <Значение скрыто>): '
            else:
                input_prompts_message = f'{prompt} (По-умолчанию: {default}): '

            if not echo_turned_on:
                value = getpass(prompt=input_prompts_message)
            else:
                value = input(input_prompts_message)

            if value == '' and not isinstance(default, ValueDefaultUnSet):
                value = default

            value = cast(value)

            self._post_input_render()

            is_valid = self.validate_value(value=value, validators=validators)

            if is_valid:
                return value
