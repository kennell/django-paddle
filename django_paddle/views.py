from django.http import HttpResponse
from .utils import webhook_signature_is_valid
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django_paddle import signals


class Webhook:
    pass


@csrf_exempt
@require_POST
def webhook(request):
    payload = request.POST.dict()

    if webhook_signature_is_valid(payload):
        alert_name = payload['alert_name']
        signal = getattr(signals, alert_name)
        if signal:
            signal.send(
                sender=Webhook,
                payload=payload
            )
        else:
            # Log warning if alert_name does not match any signal?
            pass

    return HttpResponse()
