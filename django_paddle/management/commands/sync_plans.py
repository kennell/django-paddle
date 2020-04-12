from django.core.management.base import BaseCommand
from django_paddle.models import PaddlePlan


class SyncPlans(BaseCommand):
    help = 'Sync plans'

    def handle(self, *args, **options):
        PaddlePlan.sync()
