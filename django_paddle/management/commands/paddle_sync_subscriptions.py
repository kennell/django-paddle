from django.core.management.base import BaseCommand
from django_paddle.models import PaddleSubscription


class Command(BaseCommand):
    help = 'Sync subscriptions'

    def handle(self, *args, **options):
        PaddleSubscription.sync()  # sync default
        PaddleSubscription.sync(state='deleted')  # also sync deleted
