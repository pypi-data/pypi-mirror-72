from __future__ import unicode_literals

from django.utils.module_loading import autodiscover_modules

from whisperer.events import registry
from whisperer.tasks import deliver_event


def autodiscover():
    autodiscover_modules('webhooks', register_to=registry)


default_app_config = 'whisperer.apps.WhispererConfig'
