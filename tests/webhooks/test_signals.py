from unittest.mock import MagicMock
from django.test import Client, TestCase
from django.urls import reverse
from django_paddle import signals
from django_paddle.views import Webhook
from tests.helpers import disable_webhook_verification


class TestWebhookSignals(TestCase):

    def setUp(self):
        self.client = Client()
        self.path = reverse('django_paddle_webhook')

    @disable_webhook_verification
    def test_subscription_created(self):
        receiver = MagicMock()
        signals.subscription_created.connect(receiver, sender=Webhook)
        rsp = self.client.post(
            path=self.path,
            data={
                'alert_name': 'subscription_created',
                'p_signature': 'cXdlcnR5'
            }
        )

        self.assertEqual(rsp.status_code, 200)
        receiver.assert_called_once()

