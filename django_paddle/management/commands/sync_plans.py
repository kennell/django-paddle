from django.core.management.base import BaseCommand
from django_paddle.models import PaddlePlan, PaddleInitialPrice, PaddleRecurringPrice


class SyncPlans(BaseCommand):
    help = 'Sync plans'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Sync'))
