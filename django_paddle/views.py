from django.http import HttpResponse
from .utils import webhook_signature_is_valid
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from . import signals


@csrf_exempt
@require_POST
def webhook(request):

    payload = request.POST.dict()

    if webhook_signature_is_valid(payload):
        alert_name = payload['alert_name']
        getattr(signals, alert_name).send(
            sender=None,
            payload=payload
        )

    return HttpResponse()
