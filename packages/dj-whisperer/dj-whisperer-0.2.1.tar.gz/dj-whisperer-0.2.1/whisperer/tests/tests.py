import mock
import requests
import requests_mock
from django.contrib.auth.models import User
from django.test import TestCase
from model_mommy import mommy

from whisperer.exceptions import WebhookAlreadyRegistered
from whisperer.models import Webhook, WebhookEvent
from whisperer.resources.serializers import WebhookSerializer
from whisperer.services import WebhookService
from whisperer.tests.models import Address, Customer, Order


class WebhookTestCase(TestCase):
    def setUp(self):
        self.user = mommy.make(User, username='test_user')
        self.service = WebhookService()
        self.webhook = mommy.make(
            Webhook,
            user=self.user,
            target_url='http://example2.com/order_create',
            secret_key='secret',
            event_type='order-created',
        )

    def test_register_webhook(self):
        webhook = mommy.prepare(
            Webhook,
            user=self.user,
            target_url='http://example.com/order_create',
            secret_key='secret',
            event_type='order-created',
        )

        serializer = WebhookSerializer(webhook)
        serializer = WebhookSerializer(data=serializer.data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        webhook = self.service.register_webhook(
            user=self.user, **serializer.validated_data
        )

        with self.assertRaises(WebhookAlreadyRegistered):
            webhook = self.service.register_webhook(
                user=self.user, **serializer.validated_data
            )

    def test_update_webhook(self):
        update_data = {
            'target_url': 'http://example.com/order_update',
            'event_type': 'order-update',
        }
        serializer = WebhookSerializer(self.webhook, data=update_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        webhook = self.service.update_webhook(
            self.webhook, self.user, **serializer.validated_data
        )
        self.webhook.refresh_from_db()
        self.assertEqual(self.webhook.target_url, 'http://example.com/order_update')
        self.assertEqual(self.webhook.event_type, 'order-update')

    def test_delete_webhook(self):
        webhook = mommy.make(Webhook, is_active=True)
        self.service.delete_webhook(webhook)
        webhook.refresh_from_db()
        self.assertFalse(webhook.is_active)


class WhispererEventTestCase(TestCase):
    def setUp(self):
        self.target_url = 'http://example.com/order_create'
        self.user = mommy.make(User, username='test_user')

        self.webhook = mommy.make(
            Webhook,
            user=self.user,
            target_url=self.target_url,
            secret_key='secret',
            event_type='order-created',
        )
        self.customer = mommy.make(Customer)
        self.address = mommy.make(Address)
        self.order = mommy.prepare(
            Order,
            customer=self.customer,
            address=self.address,
            number='1',
            amount='1',
            discount_amount='1',
            shipping_amount='1',
        )

    def test_deliver_event(self):
        with requests_mock.Mocker() as mock:
            mock.register_uri(
                'POST', self.target_url, text='Order Created', status_code=200
            )
            self.order.save()
            webhook_events = WebhookEvent.objects.all()
            self.assertEqual(len(webhook_events), 1)
            self.assertTrue(webhook_events[0].delivered)

    @mock.patch('requests.post')
    def test_http_error(self, post_mock):
        post_mock.side_effect = requests.exceptions.HTTPError('HTTPError')
        self.order.save()
        webhook_events = WebhookEvent.objects.all()
        self.assertEqual(len(webhook_events), 1)
        self.assertFalse(webhook_events[0].delivered)
        self.assertEqual(webhook_events[0].response_http_status, 500)
        self.assertIn("HTTPError", webhook_events[0].response_content)


def dummy_whisperer_event_callback(response, event_type, instance, payload):
    """ this function creates customer in test database """
    mommy.make(Customer)


class WhispererEventCallbackTestCase(TestCase):
    def setUp(self):
        self.target_url = 'http://example.com/foo_bar'
        user = mommy.make(User, username='test_user')
        mommy.make(
            Webhook,
            user=user,
            target_url=self.target_url,
            secret_key='secret',
            event_type='order-created',
            callback='whisperer.tests.tests.dummy_whisperer_event_callback',
        )
        customer = mommy.make(Customer)
        address = mommy.make(Address)
        self.order = mommy.prepare(
            Order,
            customer=customer,
            address=address,
            number='1',
            amount='1',
            discount_amount='1',
            shipping_amount='1',
        )

    def tearDown(self):
        Customer.objects.all().delete()

    def test_runs_callback(self):
        with requests_mock.Mocker() as mock:
            mock.register_uri(
                'POST', self.target_url, text='Request Processed', status_code=200
            )

            # before callback we have one customer
            self.assertEqual(Customer.objects.count(), 1)
            self.order.save()
            webhook_events = WebhookEvent.objects.all()
            self.assertEqual(len(webhook_events), 1)
            self.assertTrue(webhook_events[0].delivered)

            # check callback has run
            self.assertEqual(Customer.objects.count(), 2)
