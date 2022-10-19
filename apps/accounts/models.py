from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields.citext import CICharField
from django.db import models

from apps.accounts.managers import UserManager
from apps.accounts.validators import validate_username, validator_first_name, validator_last_name, validate_user_id


class User(AbstractBaseUser, PermissionsMixin):
    """
    Аккаунт пользователя сайта.
    username: Юзернейм пользователя, используется для входа.
        - Обязательное поле.
        - Регистронезависимое поле
        - Минимальная длинна три символа
        - Максимальная длинна восемь символов
        - Должно начинаться с латинской буквы, или _
        - Может сожержать латинские буквы, цифры, _

    first_name: Имя пользователя.
        - Обязательное поле
        - Может содержать любые символы

    last_name: Фамилия пользователя.
        - Может отсутствовать
        - Может содержать любые символы

    is_staff: Статус персонала.
        Имеет доступ к панеле администрировании сайта.
        - Обязательное поле

    date_registration: Дата и время регистрации аккаунта.
        - Обязательное поле
    """

    id = models.BigAutoField(
        verbose_name='AccountID',
        validators=(validate_user_id, ),
        primary_key=True,
    )
    username = CICharField(
        verbose_name='Username',
        max_length=32,
        unique=True,
        validators=(validate_username,),
        error_messages={
            'unique': 'Данное имя пользователя уже занято.',
        }
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=64,
        validators=(validator_first_name,),
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=64,
        validators=(validator_last_name,),
        default='',
        blank=True,

    )

    is_staff = models.BooleanField(
        verbose_name='Стату персонала',
        default=False,
        help_text='Определяет, может ли пользователь войти на этот сайт администратора.',
    )

    is_active = models.BooleanField(
        verbose_name='Aктивирован',
        default=True
    )

    date_registered = models.DateTimeField(
        verbose_name='Дата и время регистрации аккаунта',
        auto_now_add=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('first_name',)
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        swappable = 'AUTH_USER_MODEL'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        full_name = self.first_name
        if self.last_name:
            full_name += f'{self.last_name}'
        return full_name