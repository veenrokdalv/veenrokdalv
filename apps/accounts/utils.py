from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

UserModel = get_user_model()


def get_random_username() -> str:
    prefix = 'user_'
    while True:
        user_uuid = get_random_string(length=8, allowed_chars=settings.USERNAME_ALLOWED_CHARS)
        username = prefix+user_uuid
        if not UserModel.objects.filter(username=username).exists():
            return username


