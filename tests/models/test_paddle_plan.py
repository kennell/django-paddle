import responses
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

    def test_cancel(self):
        # TBI
        self.assertTrue(True)

    def test_pause(self):
        # TBI
        self.assertTrue(True)

    def test_unpause(self):
        # TBI
        self.assertTrue(True)


class TestPaddlePlanSync(TestCase):

    @responses.activate
    def test_sync_create(self):
        expected = {
            'success': True,
            'response': [
                {
                    'id': 12345,
                    'name': 'Foo',
                    'billing_type': 'month',
                    'billing_period': 1,
                    'trial_days': 14,
                    'initial_price': {
                        'USD': '10.00',
                        'EUR': '10.00'
                    },
                    'recurring_price': {
                        'USD': '10.00',
                        'EUR': '10.00'
                    }
                }
            ]
        }
        responses.add(
            method=responses.POST,
            url='https://vendors.paddle.com/api/2.0/subscription/plans',
            json=expected
        )
        PaddlePlan.sync()
        self.assertEqual(PaddlePlan.objects.count(), 1)
        self.assertEqual(PaddleInitialPrice.objects.count(), 2)
        self.assertEqual(PaddleRecurringPrice.objects.count(), 2)

    @responses.activate
    def test_sync_update(self):
        plan = PaddlePlan.objects.create(
            id=12345,
            name='Foo',
            billing_type='month',
            billing_period=1,
            trial_days=14
        )
        plan.initial_prices.create(
            currency='USD',
            amount='5.00'
        )
        plan.recurring_prices.create(
            currency='USD',
            amount='5.00'
        )
        expected = {
            'success': True,
            'response': [
                {
                    'id': 12345,
                    'name': 'Bar',
                    'billing_type': 'month',
                    'billing_period': 1,
                    'trial_days': 14,
                    'initial_price': {
                        'USD': '10.00',
                        'EUR': '10.00'
                    },
                    'recurring_price': {
                        'USD': '10.00',
                        'EUR': '10.00'
                    }
                }
            ]
        }
        responses.add(
            method=responses.POST,
            url='https://vendors.paddle.com/api/2.0/subscription/plans',
            json=expected
        )
        PaddlePlan.sync()
        plan.refresh_from_db()
        self.assertEqual(plan.name, 'Bar')
        self.assertEqual(plan.initial_price_in('USD'), '10.00')
        self.assertEqual(plan.initial_price_in('EUR'), '10.00')
        self.assertEqual(plan.recurring_price_in('USD'), '10.00')
        self.assertEqual(plan.recurring_price_in('EUR'), '10.00')
