from django.apps import AppConfig


class DjangoPaddleConfig(AppConfig):
    name = 'django_paddle'
    verbose_name = 'Django Paddle'

    def ready(self):
        from django_paddle.signals import *
