from functools import wraps
from unittest.mock import patch


def mocked_webhook_signature_is_valid(*args):
    return True


def disable_webhook_verification(f):
    @wraps(f)
    @patch('django_paddle.views.webhook_signature_is_valid', new=mocked_webhook_signature_is_valid)
    def wrapper(*args, **kwds):
        return f(*args, **kwds)
    return wrapper
