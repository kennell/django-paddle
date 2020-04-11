from django.test import TestCase
from django_paddle.models import PaddlePlan, PaddleInitialPrice, PaddleRecurringPrice


class TestPaddlePlan(TestCase):

    def setUp(self):
        self.plan = PaddlePlan.objects.create(
            id=123,
            name='Plan Foo',
            billing_type='month',
            billing_period=1,
            trial_days=14
        )

    def test_initial_price_in(self):
        PaddleInitialPrice.objects.create(
            plan=self.plan,
            currency='USD',
            amount='10.000'
        )
        self.assertEqual(self.plan.initial_price_in('USD'), '10.000')

    def test_recurring_price_in(self):
        PaddleRecurringPrice.objects.create(
            plan=self.plan,
            currency='USD',
            amount='10.000'
        )
        self.assertEqual(self.plan.recurring_price_in('USD'), '10.000')
