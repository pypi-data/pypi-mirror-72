import json

import requests
from celery import current_app
from django.apps import apps
from django.db import models
from django.utils import timezone
from rest_framework.utils.encoders import JSONEncoder

from whisperer.client import WebhookClient
from whisperer.events import registry
from whisperer.exceptions import (
    EventAlreadyDelivered,
    UnknownEventType,
    WebhookEventDoesNotExist,
)


def get_natural_key(instance):
    from django.contrib.contenttypes.models import ContentType

    content_type = ContentType.objects.get_for_model(instance)
    return content_type.natural_key()


@current_app.task(bind=True, max_retries=22)
def deliver_event_task(
    self,
    hook_id,
    event_type,
    event_uuid=None,
    instance=None,
    app_label=None,
    model_name=None,
    pk=None,
    **kwargs
):
    from whisperer.models import Webhook

    if not instance:
        model_class = apps.get_model(app_label, model_name)
        instance = model_class.objects.get(pk=pk)
        hook = Webhook.objects.get(pk=hook_id)

    webhook_event, response = _deliver_event(
        hook, instance, event_type, event_uuid=event_uuid
    )

    if not response.ok:
        self.request.kwargs['event_uuid'] = webhook_event.uuid
        if len(webhook_event.request_datetimes) >= 22:
            return

        self.retry(countdown=2 ** self.request.retries)


def _deliver_event(hook, instance, event_type, event_uuid=None, force=False):
    from whisperer.models import WebhookEvent

    if event_type not in registry:
        raise UnknownEventType()

    if event_uuid:
        try:
            webhook_event = WebhookEvent.objects.get(uuid=event_uuid)
            if webhook_event.delivered and not force:
                raise EventAlreadyDelivered()
        except WebhookEvent.DoesNotExist:
            raise WebhookEventDoesNotExist()
    else:
        webhook_event = WebhookEvent(webhook=hook)

    event_class = registry[event_type]
    event = event_class()
    serialize_instance = event.serialize(instance)
    payload = {
        'event': {'type': event_type, 'uuid': webhook_event.uuid.hex},
        'payload': serialize_instance,
    }
    request_datetime = timezone.now()
    try:
        client = WebhookClient(event_type=event_type, payload=payload)
        response = client.send_payload(
            target_url=hook.target_url,
            payload=payload,
            secret_key=hook.secret_key,
            additional_headers=hook.additional_headers,
        )
    except requests.exceptions.RequestException as exc:
        response = requests.Response()
        response.status_code = (exc.response and exc.response.status_code) or 500
        response._content = exc
    finally:
        webhook_event.request_payload = json.loads(json.dumps(payload, cls=JSONEncoder))
        webhook_event.response_content = response.content
        webhook_event.response_http_status = response.status_code
        if 200 <= response.status_code < 300:
            webhook_event.delivered = True
        else:
            webhook_event.delivered = False
        webhook_event.request_datetimes.insert(0, request_datetime)
        webhook_event.save()

    if hook.callback:
        from django.utils.module_loading import import_string

        callback_function = import_string(hook.callback)
        callback_function(response, event_type, instance, payload)

    return webhook_event, response


def deliver_event(instance, event_type, async_=True):
    from whisperer.models import Webhook

    hooks = Webhook.objects.filter(event_type=event_type, is_active=True)
    for hook in hooks:
        if not async_:
            _deliver_event(hook, instance, event_type)
            continue
        if isinstance(instance, (models.Model, models.base.ModelBase)):
            app_label, model_name = get_natural_key(instance)
            deliver_event_task.delay(
                hook_id=hook.pk,
                event_type=event_type,
                app_label=app_label,
                model_name=model_name,
                pk=instance.pk,
            )
        elif isinstance(instance, dict):
            deliver_event_task.delay(
                hook_id=hook.pk, event_type=event_type, instance=instance
            )
        else:
            raise NotImplementedError()
