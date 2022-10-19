from apps.accounts.validators import validate_user_id, validate_username, validate_email
from apps.core.exceptions import InvalidData


def is_login_valid(login: str | int) -> bool:

    try:
        validate_user_id(login)
    except InvalidData:
        pass
    else:
        return True

    try:
        validate_email(login)
    except InvalidData:
        pass
    else:
        return True

    try:
        validate_username(login)
    except InvalidData:
        pass
    else:
        return True

    return False




