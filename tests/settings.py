SECRET_KEY = 'fake-key'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}
INSTALLED_APPS = [
    'django_paddle'
]
PADDLE_VENDOR_ID = '12345'
PADDLE_AUTH_CODE = 'very-secret-auth-code'