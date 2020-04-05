from django.core.management.base import BaseCommand


class SyncPlans(BaseCommand):
    help = 'Sync plans'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Sync'))