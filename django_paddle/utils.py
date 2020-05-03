import base64
import collections
import json

import phpserialize
from cryptography import exceptions
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from django.conf import settings
from django.apps import apps


def get_account_model():
    app, model = settings.PADDLE_ACCOUNT_MODEL.split('.')
    return apps.get_model(app, model, require_ready=False)


def get_account_by_passthrough(passthrough):
    if passthrough:
        try:
            passthrough = json.loads(passthrough)
            account_id = passthrough['account_id']
        except json.decoder.JSONDecodeError:
            account_id = passthrough
    else:
        account_id = None

    try:
        account = get_account_model().objects.get(id=account_id)
    except get_account_model().DoesNotExist:
        account = None

    return account


def webhook_signature_is_valid(payload):

    signature = base64.b64decode(payload.pop('p_signature'))

    for field in payload:
        payload[field] = str(payload[field])

    sorted_data = collections.OrderedDict(sorted(payload.items()))
    serialized_data = phpserialize.dumps(sorted_data)

    public_key = load_pem_public_key(settings.PADDLE_PUBLIC_KEY.encode(), backend=default_backend())

    try:
        public_key.verify(
            signature=signature,
            data=serialized_data,
            padding=PKCS1v15(),
            algorithm=SHA1()
        )
        return True
    except exceptions.InvalidSignature:
        return False
