from django.db import models


class Plan(models.Model):

    id = models.PositiveIntegerField()
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
