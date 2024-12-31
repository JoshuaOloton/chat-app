import re
from uuid import UUID


def is_valid_email(email: str):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_regex, email):
        return False

    return True

def is_valid_password(password: str):
    """ Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character. """
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$'

    if not re.match(password_regex, password):
        return False

    return True


def is_valid_uuid(uuid_id):
    try:
        uuid_obj = UUID(uuid_id, version=4)
        return str(uuid_obj) == uuid_id
    except ValueError:
        return False


