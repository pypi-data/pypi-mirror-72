Introduction
============

Installation
------------

You can install this package from `PyPI <https://pypi.org/>`_::

    pip install dj-whisperer

You need to append it to the ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'whisperer',
    ]


Then migrate your project::

    python manage.py migrate whisperer

Now you are ready to create your whisperer events, take a look at :doc:`quickstart`.
