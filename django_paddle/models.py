from django.db import models


class PaddlePlan(models.Model):
    id = models.PositiveIntegerField(
        primary_key=True,
        unique=True
    )
    name = models.CharField(max_length=255)
    billing_period = models.PositiveIntegerField()
    billing_type = models.CharField(max_length=255)

    def initial_price_in(self, currency):
        return self.initial_prices.get(currency=currency).amount

    def recurring_price_in(self, currency):
        return self.recurring_prices.get(currency=currency).amount

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.id)


class PaddlePrice(models.Model):
    plan = models.ForeignKey(
        to=PaddlePlan,
        on_delete=models.CASCADE,
    )
    currency = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.currency)

    class Meta:
        abstract = True
        unique_together = ['plan', 'currency']


class PaddleInitialPrice(PaddlePrice):
    class Meta:
        default_related_name = 'initial_prices'


class PaddleRecurringPrice(PaddlePrice):

    class Meta:
        default_related_name = 'recurring_prices'
