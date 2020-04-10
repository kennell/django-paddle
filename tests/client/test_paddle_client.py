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
                    'initial_price':
                        {
                            'USD': '10.00',
                            'EUR': '10.00'
                        },
                    'recurring_price':
                        {
                            'USD': '10.00',
                            'EUR': '10.00'
                        },
                    'trial_days': 14
                }
            ]
        }
        responses.add(
            method=responses.POST,
            url='https://vendors.paddle.com/api/2.0/subscription/plans',
            json=expected
        )
        self.assertDictEqual(
            self.client.plans_list(), expected
        )