from datetime import datetime
from django.dispatch import receiver
from django.utils.timezone import make_aware
from .signals import subscription_created
from .models import PaddlePlan, PaddleSubscription
from .utils import get_account_by_passthrough


@receiver(subscription_created)
def subscription_created_receiver(**kwargs):
    payload = kwargs['payload']

    account = get_account_by_passthrough(payload['passthrough'])

    try:
        plan = PaddlePlan.objects.get(id=payload['subscription_plan_id'])
    except PaddlePlan.DoesNotExist:
        plan = None

    PaddleSubscription.objects.create(
        id=payload['subscription_id'],
        account=account,
        plan=plan,
        user_id=payload['user_id'],
        user_email=payload['email'],
        marketing_consent=payload['marketing_consent'] == True,
        update_url=payload['update_url'],
        cancel_url=payload['cancel_url'],
        state=payload['status'],
        signup_date=make_aware(datetime.strptime(payload['event_time'], '%Y-%m-%d %H:%M:%S'))
    )
