from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager


class UserManager(DjangoUserManager):
    def _create_user(self, username, password, **extra_fields):
        assert username, ValueError
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save()
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        if extra_fields.setdefault("is_staff", True) is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.setdefault("is_superuser", True) is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)

    def get_by_natural_key(self, username: str):
        from apps.accounts.services import get_user_by_login
        return get_user_by_login(username)
