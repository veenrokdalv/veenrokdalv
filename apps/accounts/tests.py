import string

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from django.utils.crypto import get_random_string

from apps.accounts.services import create_user, get_user_by_id, get_user_by_username, get_user_by_email, \
    get_user_by_login
from apps.accounts.utils import get_random_username
from apps.core.exceptions import ServiceNotAvailable


class ServicesTestCase(TestCase):
    def setUp(self) -> None:
        self.user = create_user(
            username='username',
            first_name='first name',
            password=get_random_string(length=8)
        )

    def test_create_user_by_valid_data(self):
        """
        Тестировавание создания нового пользователя с валидными данными. 
        """""
        user_data_1 = {
            'username': get_random_string(length=5, allowed_chars=string.ascii_letters),
            'first_name': get_random_string(length=5),
            'last_name': '',
            'password': get_random_string(length=32)
        }
        user_data_2 = {
            'username': get_random_string(length=3, allowed_chars=string.ascii_letters),
            'first_name': get_random_string(length=5),
            'last_name': get_random_string(length=8),
            'password': get_random_string(length=8)

        }
        user_data_3 = {
            'username': get_random_username(),
            'first_name': get_random_string(length=5),
            'password': get_random_string(length=32)
        }
        user_1 = create_user(**user_data_1)
        user_2 = create_user(**user_data_2)
        user_3 = create_user(**user_data_3)

        self.assertEqual(user_1.username, user_data_1['username'])
        self.assertEqual(user_1.first_name, user_data_1['first_name'])
        self.assertEqual(user_1.last_name, user_data_1['last_name'])
        self.assertTrue(user_1.check_password(user_data_1['password']))

        self.assertEqual(user_2.username, user_data_2['username'])
        self.assertEqual(user_2.first_name, user_data_2['first_name'])
        self.assertEqual(user_2.last_name, user_data_2['last_name'])
        self.assertTrue(user_2.check_password(user_data_2['password']))

        self.assertEqual(user_3.username, user_data_3['username'])
        self.assertEqual(user_3.first_name, user_data_3['first_name'])
        self.assertEqual(user_3.last_name, '')
        self.assertTrue(user_3.check_password(user_data_3['password']))

    def test_create_user_by_invalid_data(self):
        # Не корректный username
        invalid_username_1 = {
            'username': get_random_string(length=1, allowed_chars=string.ascii_letters),
            'first_name': get_random_string(length=5),
            'last_name': None,
            'password': get_random_string(length=32)
        }
        invalid_username_2 = {
            'username': get_random_string(length=128, allowed_chars=string.ascii_letters),
            'first_name': get_random_string(length=5),
            'last_name': None,
            'password': get_random_string(length=32)
        }
        invalid_username_3 = {
            'username': get_random_string(length=5, allowed_chars=string.digits),
            'first_name': get_random_string(length=5),
            'last_name': None,
            'password': get_random_string(length=32)
        }

        # Не корректный first_name.
        invalid_first_name_1 = {
            'username': get_random_username(),
            'first_name': '',
            'last_name': None,
            'password': get_random_string(length=32)
        }

        invalid_first_name_2 = {
            'username': get_random_username(),
            'first_name': get_random_string(length=128),
            'last_name': None,
            'password': get_random_string(length=32)
        }

        # Не корректный last_name.

        invalid_last_name_1 = {
            'username': get_random_username(),
            'first_name': get_random_string(length=8),
            'last_name': get_random_string(length=128),
            'password': get_random_string(length=32)
        }

        self.assertRaises(ValidationError, create_user, **invalid_username_1)
        self.assertRaises(ValidationError, create_user, **invalid_username_2)
        self.assertRaises(ValidationError, create_user, **invalid_username_3)
        self.assertRaises(ValidationError, create_user, **invalid_first_name_1)
        self.assertRaises(ValidationError, create_user, **invalid_first_name_2)
        self.assertRaises(ValidationError, create_user, **invalid_last_name_1)

    def test_user_get_by_id(self):
        """Тестирование получения пользователя по UserId"""
        self.assertTrue(self.user, get_user_by_id(user_id=self.user.id))
        self.assertTrue(self.user, get_user_by_id(user_id=str(self.user.id)))

        self.assertRaises(ObjectDoesNotExist, get_user_by_id, user_id=self.user.id + 1)

    def test_user_get_by_username(self):
        """Тестирование получения пользователя по Username"""
        self.assertTrue(self.user, get_user_by_username(username=self.user.username))
        self.assertTrue(self.user, get_user_by_username(username=self.user.username.upper()))

        self.assertRaises(ObjectDoesNotExist, get_user_by_username, username=f'incorrect_{self.user.username}')

    def test_user_get_by_email(self):
        """Тестирование получения пользователя по Email"""

        self.assertRaises(ServiceNotAvailable, get_user_by_email, email='username@domain.com')

    def test_user_get_by_login(self):
        """Тестирование получения пользователя по Login"""

        self.assertTrue(self.user, get_user_by_login(login=self.user.id))
        self.assertTrue(self.user, get_user_by_login(login=str(self.user.id)))
        self.assertTrue(self.user, get_user_by_login(login=self.user.username))
        self.assertRaises(ServiceNotAvailable, get_user_by_login, login='username@dimain.com')

        self.assertRaises(ObjectDoesNotExist, get_user_by_login, login=self.user.id + 1)
        self.assertRaises(ObjectDoesNotExist, get_user_by_login, login=f'_{self.user.username}')
        self.assertRaises(ServiceNotAvailable, get_user_by_login, login='username@dimain.com')


class UserSignInTestCase(TestCase):

    def setUp(self):
        self.user_raw_password = 'password'
        self.user = create_user(
            username='username',
            first_name='first name',
            password=self.user_raw_password
        )

    def test_sign_in_by_id(self):
        """Тестирование аунтетификации по UserId"""
        with self.settings(AUTHENTICATION_BACKENDS=('apps.accounts.backends.auth_backends.UserIdAndPasswordBackend',)):
            self.assertTrue(self.client.login(user_id=self.user.id, password=self.user_raw_password))
            self.assertTrue(self.client.login(user_id=str(self.user.id), password=self.user_raw_password))
            self.assertFalse(self.client.login(user_id=self.user.id, password='incorrect_password'))
            self.assertRaises(
                ValueError, self.client.login, user_id='invalid_user_id', password=self.user_raw_password
            )
            self.assertFalse(self.client.login(user_id=self.user.id, password=None))
            self.assertFalse(self.client.login(user_id=None, password=self.user_raw_password))
            self.assertFalse(self.client.login(user_id=None, password=None))

    def test_sign_in_by_username(self):
        """Тестирование аунтетификации по Username"""
        with self.settings(
                AUTHENTICATION_BACKENDS=('apps.accounts.backends.auth_backends.CIUsernameAndPasswordBackend',)):
            self.assertTrue(self.client.login(username=self.user.username, password=self.user_raw_password))
            self.assertTrue(self.client.login(username=self.user.username.upper(), password=self.user_raw_password))

            self.assertFalse(self.client.login(username=self.user.username, password='incorrect_password'))

            self.assertFalse(self.client.login(username='1_invalid_username', password=self.user_raw_password))

            self.assertFalse(self.client.login(username=self.user.username, password=None))
            self.assertFalse(self.client.login(username=None, password=self.user_raw_password))
            self.assertFalse(self.client.login(username=None, password=None))

    def test_sign_in_by_email(self):
        """Тестирование аунтетификации по Email"""
        with self.settings(AUTHENTICATION_BACKENDS=('apps.accounts.backends.auth_backends.CIEmailAndPasswordBackend',)):
            self.assertRaises(
                ServiceNotAvailable, self.client.login, email=self.user.username, password=self.user_raw_password
            )
            self.assertRaises(
                ServiceNotAvailable, self.client.login, email=self.user.username.upper(),
                password=self.user_raw_password
            )

            self.assertRaises(
                ServiceNotAvailable, self.client.login, email=self.user.username, password='incorrect_password'
            )

            self.assertRaises(
                ServiceNotAvailable, self.client.login, email='1_invalid_username', password=self.user_raw_password
            )

            self.assertFalse(self.client.login(email=self.user.username, password=None))
            self.assertFalse(self.client.login(email=None, password=self.user_raw_password))
            self.assertFalse(self.client.login(email=None, password=None))

    def test_sign_in_by_login(self):
        """Тестирование аунтетификации по Login"""
        with self.settings(AUTHENTICATION_BACKENDS=('apps.accounts.backends.auth_backends.LoginAndPasswordBackend',)):
            self.assertTrue(self.client.login(login=self.user.id, password=self.user_raw_password))
            self.assertTrue(self.client.login(login=self.user.username, password=self.user_raw_password))
            self.assertRaises(
                ServiceNotAvailable, self.client.login, login='user@domain.com', password=self.user_raw_password
            )

            self.assertFalse(self.client.login(login=self.user.id, password=None))
            self.assertFalse(self.client.login(login=self.user.username, password=None))
            self.assertFalse(self.client.login(login='user@domain.com', password=None))
            self.assertFalse(self.client.login(login=None, password=self.user_raw_password))
            self.assertFalse(self.client.login(login=None, password=None))
