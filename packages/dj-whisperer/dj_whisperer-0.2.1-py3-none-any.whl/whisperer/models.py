import uuid

from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models


class StarterModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)

    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', None)
        if update_fields is not None:
            if not isinstance(update_fields, list):
                update_fields = list(update_fields)
            update_fields.append('modified_date')
            kwargs['update_fields'] = update_fields
        super(StarterModel, self).save(*args, **kwargs)


class Webhook(StarterModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    target_url = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    secret_key = models.CharField(max_length=124, null=True, blank=True)
    event_type = models.CharField(max_length=124)
    callback = models.CharField(max_length=64, null=True, blank=True)
    additional_headers = JSONField(default=dict)

    def __str__(self):
        return '{}:{}'.format(self.event_type, self.target_url[:25])

    class Meta:
        unique_together = [('user', 'target_url', 'event_type')]


class WebhookEvent(StarterModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    webhook = models.ForeignKey(Webhook, on_delete=models.PROTECT)
    request_payload = JSONField(default=dict)
    response_content = models.TextField()
    response_http_status = models.IntegerField()
    delivered = models.BooleanField(default=False)
    request_datetimes = ArrayField(
        models.DateTimeField(null=True, blank=True), default=list
    )

    def __str__(self):
        return '{}:{}'.format(self.webhook, self.delivered)
