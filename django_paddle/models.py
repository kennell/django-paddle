from django.db import models


class Plan(models.Model):

    id = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField()
    trial_days = models.PositiveIntegerField()
    billing_period = models.PositiveIntegerField()
    billing_type = models.CharField()


class InitialPrice(models.Model):

    plan = models.ForeignKey(
        to=Plan,
        on_delete=models.CASCADE,
    )
    currency = models.CharField()
    amount = models.CharField()


class RecurringPrice(models.Model):

    plan = models.ForeignKey(
        to=Plan,
        on_delete=models.CASCADE
    )
    currency = models.CharField()
    amount = models.CharField()
