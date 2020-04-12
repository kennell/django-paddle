import responses
from django.test import TestCase

from django_paddle.client import PaddleClient


class TestPaddleClient(TestCase):

    def setUp(self):
        self.client = PaddleClient()

    @responses.activate
    def test_plans_list(self):
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
        self.assertListEqual(
            self.client.plans_list(), expected['response']
        )

    @responses.activate
    def test_subscriptions_list(self):
        expected = {
            'success': True,
            'response': [
                {
                    'subscription_id': 12345,
                    'plan_id': 12345,
                    'user_id': 12345,
                    'user_email': 'foo@example.com',
                    'marketing_consent': True,
                    'update_url': 'https://checkout.paddle.com/subscription/update?foo=bar&qux=baz',
                    'cancel_url': 'https://checkout.paddle.com/subscription/cancel?foo=bar&qux=baz',
                    'state': 'active',
                    'signup_date': '2020-01-01 20:20:20',
                    'last_payment': {
                        'amount': 0,
                        'currency': 'USD',
                        'date': '2019-11-10'
                    },
                    'linked_subscriptions': []
                }
            ]
        }
        responses.add(
            method=responses.POST,
            url='https://vendors.paddle.com/api/2.0/subscription/users',
            json=expected
        )
        self.assertListEqual(
            self.client.subscriptions_list(), expected['response']
        )

    @responses.activate
    def test_subscriptions_list_pagination(self):
        responses.add(
            method=responses.POST,
            url='https://vendors.paddle.com/api/2.0/subscription/users',
            json={
                'success': True,
                'response': [{} for _ in range(0, 200)]
            }
        )
        responses.add(
            method=responses.POST,
            url='https://vendors.paddle.com/api/2.0/subscription/users',
            json={
                'success': True,
                'response': [{} for _ in range(0, 123)]
            }
        )
        data = self.client.subscriptions_list()
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(len(data), 323)
