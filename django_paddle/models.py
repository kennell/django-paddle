from datetime import datetime

from django.db import models
from django.utils.timezone import make_aware
from django_paddle.client import PaddleClient
from django_paddle.utils import get_account_model, get_account_by_passthrough



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
    account = models.ForeignKey(
        to=get_account_model(),
        null=True,
        on_delete=models.SET_NULL,
        related_name='subscriptions'
    )
    plan = models.ForeignKey(
        to=PaddlePlan,
        null=True,
        on_delete=models.SET_NULL,
        related_name='subscriptions'
    )
    user_id = models.PositiveIntegerField()
    user_email = models.EmailField()
    marketing_consent = models.BooleanField()
    update_url = models.CharField(max_length=255)
    cancel_url = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    signup_date = models.DateTimeField()

    def cancel(self):
        pc.subscriptions_cancel(self.id)
        self.state = 'deleted'
        self.save()

    def pause(self):
        pc.subscriptions_pause(subscription_id=self.id)
        self.state = 'paused'
        self.save()

    def unpause(self):
        pc.subscriptions_unpause(subscription_id=self.id)
        self.state = 'active'
        self.save()

    @staticmethod
    def sync():
        for sub in pc.subscriptions_list():

            transaction = pc.transactions_list(entity='subscription', id=sub['subscription_id'])[0]
            account = get_account_by_passthrough(transaction['passthrough'])

            try:
                plan = PaddlePlan.objects.get(id=sub['plan_id'])
            except PaddlePlan.DoesNotExist:
                plan = None

            defaults = {
                    'user_id': sub['user_id'],
                    'user_email': sub['user_email'],
                    'marketing_consent': sub['marketing_consent'],
                    'update_url': sub['update_url'],
                    'cancel_url': sub['cancel_url'],
                    'state': sub['state'],
                    'signup_date': make_aware(datetime.strptime(sub['signup_date'], '%Y-%m-%d %H:%M:%S'))
            }

            if plan:
                defaults['plan'] = plan

            if account:
                defaults['account'] = account

            PaddleSubscription.objects.update_or_create(
                id=sub['subscription_id'],
                defaults=defaults
            )


class PaddlePayment(models.Model):
    id = models.PositiveIntegerField(
        unique=True,
        primary_key=True
    )
    subscription = models.ForeignKey(
        to=PaddleSubscription,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=255)
    payout_date = models.CharField(max_length=255)
    is_paid = models.BooleanField()
    is_one_off_charge = models.BooleanField()
    receipt_url = models.CharField(max_length=255)
