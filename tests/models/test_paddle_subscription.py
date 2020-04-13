import responses
from django.test import TestCase
from django_paddle.models import PaddleSubscription, PaddlePlan


class TestPaddleSubscription(TestCase):

    def setUp(self):
        self.plan = PaddleSubscription.objects.create(
            id=12345,
            plan=PaddlePlan.objects.create(
                id=123,
                name='Plan Foo',
                billing_type='month',
                billing_period=1,
                trial_days=14
            ),
            user_id=12345,
            user_email='foo@example.com',
            marketing_consent=True,
            update_url='https://checkout.paddle.com/subscription/update?foo=bar&qux=baz',
            cancel_url='https://checkout.paddle.com/subscription/cancel?foo=bar&qux=baz',
            state='active',
            signup_date='2020-01-01 20:20:20'
        )

    @responses.activate
    def test_subscription_cancel(self):
        responses.add(
            method=responses.POST,
            url='https://vendors.paddle.com/api/2.0/subscription/users_cancel',
            json={
                'success': True
            }
        )
        self.plan.cancel()
        self.plan.refresh_from_db()
        self.assertEqual(self.plan.state, 'deleted')

    @responses.activate
    def test_subscription_pause(self):
        # TBI
        self.assertTrue(True)

    @responses.activate
    def test_subscription_unpause(self):
        # TBI
        self.assertTrue(True)