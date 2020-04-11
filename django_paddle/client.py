import requests
from django.conf import settings


class PaddleClient:

    def __init__(self):
        self.base_url = 'https://vendors.paddle.com/api/2.0/'
        self.vendor_id = settings.PADDLE_VENDOR_ID
        self.vendor_auth_code = settings.PADDLE_AUTH_CODE
        self.payload = {
            'vendor_id': self.vendor_id,
            'vendor_auth_code': self.vendor_auth_code
        }

    def plans_list(self):
        rsp = requests.post(
            url=self.base_url + 'subscription/plans',
            json=self.payload
        )
        return rsp.json()['response']
