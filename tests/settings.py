SECRET_KEY = 'fake-key'

ROOT_URLCONF = 'tests.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django_paddle'
]

PADDLE_VENDOR_ID = '12345'
PADDLE_AUTH_CODE = 'very-secret-auth-code'
PADDLE_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgFRcEWH8FJB0UnbD7Owhl6anraQS
/5xrqyPyLkjR3Xb9/WsvrA1eP3ePg+vKdypMD+1puGg2/ler8aDi1OmvWC031ERs
06LHL628aVMvu1n6nZyKtvoFJpYTxBE804Evf6FSH5C+oba2BH6fEW9BxtraK7Co
SKoHy0wFWqzUHsBBAgMBAAE=
-----END PUBLIC KEY-----"""
PADDLE_ACCOUNT_MODEL='auth.User'