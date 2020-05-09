from django.core.management.base import BaseCommand
from django_paddle.models import PaddleSubscription, PaddlePayment


class Command(BaseCommand):
    help = 'Sync payments'

    def handle(self, *args, **options):
        for subscription in PaddleSubscription.objects.all():
            subscription.sync_payments()
