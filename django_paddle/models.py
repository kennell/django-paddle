from django.db import models
from django_paddle.client import PaddleClient


pc = PaddleClient()


class PaddlePlan(models.Model):
    id = models.PositiveIntegerField(
        primary_key=True,
        unique=True
    )
    name = models.CharField(max_length=255)
    billing_type = models.CharField(max_length=255)
    billing_period = models.PositiveIntegerField()
    trial_days = models.PositiveIntegerField()

    def initial_price_in(self, currency):
        return self.initial_prices.get(currency=currency).amount

    def recurring_price_in(self, currency):
        return self.recurring_prices.get(currency=currency).amount

    @staticmethod
    def sync():
        for plan in pc.plans_list():
            plan_obj, _ = PaddlePlan.objects.update_or_create(
                id=plan['id'],
                defaults={
                    'name': plan['name'],
                    'billing_type': plan['billing_type'],
                    'billing_period': plan['billing_period'],
                    'trial_days': plan['trial_days']
                }
            )
            for currency, amount in plan['initial_price'].items():
                plan_obj.initial_prices.update_or_create(
                    currency=currency,
                    defaults={
                        'amount': amount
                    }
                )
            for currency, amount in plan['recurring_price'].items():
                plan_obj.recurring_prices.update_or_create(
                    currency=currency,
                    defaults={
                        'amount': amount
                    }
                )


class PaddlePrice(models.Model):
    plan = models.ForeignKey(
        to=PaddlePlan,
        on_delete=models.CASCADE,
    )
    currency = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)

    class Meta:
        abstract = True
        unique_together = ['plan', 'currency']


class PaddleInitialPrice(PaddlePrice):
    class Meta:
        default_related_name = 'initial_prices'


class PaddleRecurringPrice(PaddlePrice):

    class Meta:
        default_related_name = 'recurring_prices'


class PaddleSubscription(models.Model):
    id = models.PositiveIntegerField(
        primary_key=True,
        unique=True
    )
    plan = models.ForeignKey(to=PaddlePlan, null=True, on_delete=models.SET_NULL)
    user_id = models.PositiveIntegerField()
    user_email = models.EmailField()
    marketing_consent = models.BooleanField()
    update_url = models.CharField(max_length=255)
    cancel_url = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    signup_date = models.DateTimeField()
