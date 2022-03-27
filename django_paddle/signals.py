from django.dispatch import Signal


class WebhookSignalFactory():

    def __new__(self):
        return Signal()


# Subscriptions
subscription_created = WebhookSignalFactory()
subscription_updated = WebhookSignalFactory()
subscription_cancelled = WebhookSignalFactory()
subscription_payment_succeeded = WebhookSignalFactory()
subscription_payment_failed = WebhookSignalFactory()
subscription_payment_refunded = WebhookSignalFactory()

# One-off Purchases
locker_processed = WebhookSignalFactory()
payment_succeeded = WebhookSignalFactory()
payment_refunded = WebhookSignalFactory()

# Risk & Dispute Alerts
payment_dispute_created = WebhookSignalFactory()
payment_dispute_closed = WebhookSignalFactory()
high_risk_transaction_created = WebhookSignalFactory()
high_risk_transaction_updated = WebhookSignalFactory()

# Payout Alerts
transfer_created = WebhookSignalFactory()
transfer_paid = WebhookSignalFactory()

# Audience Alerts
new_audience_member = WebhookSignalFactory()
update_audience_member = WebhookSignalFactory()
