import responses
from datetime import timedelta
from django.test import TestCase
from django_paddle.models import PaddleSubscription, PaddlePlan
from django.utils import timezone


class TestPaddleSubscription(TestCase):

    def setUp(self):
        self.subscription = PaddleSubscription.objects.create(
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
            signup_date='2020-01-01 20:20:20',
            cancellation_effective_date=None
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
        self.subscription.cancel()
        self.subscription.refresh_from_db()
        self.assertEqual(self.subscription.state, 'deleted')

    @responses.activate
    def test_subscription_pause(self):
        # TBI
        self.assertTrue(True)

    @responses.activate
    def test_subscription_unpause(self):
        # TBI
        self.assertTrue(True)


class TestPaddleSubscriptionIsCanceled(TestCase):

    """
    Tests the is_canceled property
    """

    def setUp(self):
        self.subscription = PaddleSubscription.objects.create(
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
            signup_date='2020-01-01 20:20:20',
            cancellation_effective_date=None
        )

    def test_is_canceled_cancellation_effective_date_is_null(self):
        self.subscription.cancellation_effective_date = None
        self.subscription.save()
        self.assertFalse(self.subscription.is_canceled)

    def test_is_canceled_cancellation_effective_date_is_set(self):
        self.subscription.cancellation_effective_date = timezone.now()
        self.subscription.save()
        self.assertTrue(self.subscription.is_canceled)


class TestPaddleSubscriptionIsActive(TestCase):

    """
    Tests the is_active property
    """

    def setUp(self):
        self.subscription = PaddleSubscription.objects.create(
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
            signup_date='2020-01-01 20:20:20',
            cancellation_effective_date=None
        )

    def test_is_active(self):
        self.subscription.state = 'active'
        self.subscription.save()
        self.assertTrue(self.subscription.is_active)

    def test_is_active_deleted_no_cancellation_date(self):
        self.subscription.state = 'deleted'
        self.subscription.cancellation_effective_date = None
        self.subscription.save()
        self.assertFalse(self.subscription.is_active)

    def test_is_active_cancellation_date_in_future(self):
        self.subscription.state = 'deleted'
        self.subscription.cancellation_effective_date = timezone.now() + timedelta(days=3)
        self.subscription.save()
        self.assertTrue(self.subscription.is_active)

    def test_is_active_cancellation_date_in_past(self):
        self.subscription.state = 'deleted'
        self.subscription.cancellation_effective_date = timezone.now() - timedelta(days=3)
        self.subscription.save()
        self.assertFalse(self.subscription.is_active)