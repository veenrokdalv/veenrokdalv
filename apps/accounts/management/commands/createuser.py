from distutils.util import strtobool

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import get_password_validators
from django.core.management import CommandParser, CommandError
from django.template.defaultfilters import yesno
from django.utils.crypto import get_random_string

from apps.accounts.services import create_user
from apps.accounts.utils import get_random_username
from apps.core.management.commands._private import ExtendedBaseCommand

PASSWORD_FIELD_NAME = 'password'


class Command(ExtendedBaseCommand):
    """Создать пользователя"""
    help = 'Created user'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            f'--{self.UserModel.USERNAME_FIELD}',
            help=self.UserModel._meta.get_field(self.UserModel.USERNAME_FIELD).help_text,
            default=None
        )
        for field_name in self.UserModel.REQUIRED_FIELDS:
            field = self.UserModel._meta.get_field(field_name)
            field_arg_name = field_name.replace('_', '-')
            if field.many_to_many:
                if (
                        field.remote_field.through
                        and not field.remote_field.through._meta.auto_created
                ):
                    raise CommandError(
                        f'Обязательное поле {field_name} указывает много-ко-многим '
                        'связь через модель, которая не поддерживается.'
                    )
                else:
                    parser.add_argument(
                        f'--{field_arg_name}',
                        help=field.help_text,
                        default=None
                    )
            else:
                parser.add_argument(
                    f'--{field_arg_name}',
                    help=field.help_text
                )

        parser.add_argument(
            f'--{PASSWORD_FIELD_NAME}',
            default=None
        )

        parser.add_argument(
            '--output-password',
            '-op',
            action='store_true',
            default=False
        )

        parser.add_argument(
            '--set-staff',
            '-s',
            action='store_true',
            default=False
        )

        parser.add_argument(
            '--set-superuser',
            '-S',
            action='store_true',
            default=False
        )

        parser.add_argument(
            '--random',
            '-r',
            action='store_true',
            default=False
        )

    def handle(self, *args, **options):
        input_data = {}

        if options[self.UserModel.USERNAME_FIELD]:
            field = self.UserModel._meta.get_field(self.UserModel.USERNAME_FIELD)
            input_data[self.UserModel.USERNAME_FIELD] = options[self.UserModel.USERNAME_FIELD]
            self.validate_value(input_data[self.UserModel.USERNAME_FIELD], field.validators)
        elif options['random']:
            input_data[self.UserModel.USERNAME_FIELD] = get_random_username()
        else:
            field = self.UserModel._meta.get_field(self.UserModel.USERNAME_FIELD)

            input_data[self.UserModel.USERNAME_FIELD] = self.input(
                prompt=field.verbose_name,
                validators=field.validators,
                default=get_random_username()
            )
        for field_name in self.UserModel.REQUIRED_FIELDS:
            field = self.UserModel._meta.get_field(field_name)

            if options[field_name]:
                input_data[field_name] = options[field_name]
                field = self.UserModel._meta.get_field(field_name)
                self.validate_value(input_data[field_name], field.validators)
            elif options['random']:
                input_data[field_name] = get_random_string(length=8)
            else:
                input_data[field_name] = self.input(
                    prompt=field.verbose_name,
                    validators=field.validators,
                )

        if options[PASSWORD_FIELD_NAME]:
            input_data[PASSWORD_FIELD_NAME] = options[PASSWORD_FIELD_NAME]
        elif options['random']:
            input_data[PASSWORD_FIELD_NAME] = get_random_string(length=8)
        else:
            input_data[PASSWORD_FIELD_NAME] = self._input_password(echo_turned_on=options['output_password'])

        self.create_user(args=args, options=options, input_data=input_data)

    def create_user(self, args, options, input_data):
        try:
            user = create_user(
                is_staff=options['set_staff'], is_superuser=options['set_superuser'], **input_data, commit=True,
            )
        except Exception as error:
            self.stderr.write('Пользователь не создан!')
            self.render_input_error(error=error)
        else:
            self._render_user_info(args, options, input_data, user)

    def _render_user_info(self, args, options, input_data, user):
        renderer_info_required_fields = ''
        for field_name in self.UserModel.REQUIRED_FIELDS:
            renderer_info_required_fields += (
                f'{self.UserModel._meta.get_field(field_name).verbose_name}: {getattr(user, field_name)}\n'
            )
        self.stdout.write(self.style.SUCCESS(f'Пользователь {user.username} создан!'))
        self.stdout.write(
            f'{self.UserModel.id.field.verbose_name}: {user.id}\n'
            f'{self.UserModel._meta.get_field(self.UserModel.USERNAME_FIELD).verbose_name}: {user.username}\n'
            f'{renderer_info_required_fields}'
            f'{self.UserModel.is_superuser.field.verbose_name}: {yesno(user.is_superuser, "Да,Нет")}\n'
            f'{self.UserModel.is_staff.field.verbose_name}: {yesno(user.is_staff, "Да,Нет")}'

        )
        if options['output_password']:
            self.stdout.write(
                f'Пароль: {input_data["password"]}'
            )

    def _input_password(self, echo_turned_on) -> str:

        random_password = get_random_string(length=8)
        while True:
            errors = False
            password = self.input(
                prompt='Пароль',
                default=random_password,
                echo_turned_on=echo_turned_on
            )

            if password == random_password:
                return password

            password_repeat = self.input(
                prompt='Повтор пароля',
                echo_turned_on=echo_turned_on
            )

            if password != password_repeat:
                self.stderr.write('Пароли не совпадают!')
                continue
            for validator in get_password_validators(settings.AUTH_PASSWORD_VALIDATORS):
                try:
                    validator.validate(password)
                except Exception as error:
                    self.render_input_error(error=error)
                    errors = True

            if errors:
                ignore_errors = self.input(
                    prompt='Обойти проверку пароля и создать пользователя в любом случае? [yes/no]',
                    default='yes',
                    cast=strtobool()
                )
                if ignore_errors:
                    return password
