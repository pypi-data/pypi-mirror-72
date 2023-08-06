Advanced Usage
==============

Django Whisperer app is highly extensible.

Callback Function
-----------------

When a callback function specified, it can be called after informing
subscribed user with response, event_type, instance and request payload.

.. code-block:: python

    import logging

    logger = logging.getLogger(__name__)

    def callback(response, event_type, instance, payload):
        logger.info('this is a sweety callback function.')
        # some other codes


Subscribing to an event with callback function is as follows:

.. code-block:: python

    import requests

    requests.post(
        url='https://your-app.com/whisperer/hooks/',
        headers={
            'Authorization': 'Token <secret-login-token>',
        },
        json={
            'event_type': 'package-created',
            'secret_key': '<secret>',
            'target_url': 'https://example.com/',
            'callback': 'foo.bar.app.callback'
        }
    )

