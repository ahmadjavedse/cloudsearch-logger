.. image:: https://badge.fury.io/py/CloudSearch-Logger.svg
    :target: https://pypi.python.org/pypi/CloudSearch-Logger
    :alt: PyPI Version

CloudSearch-Logger
==================
This module helps you in logging data on amazon cloudsearch server using python logger.

Installing
----------
When ``pip`` is available, the distribution can be downloaded from PyPI and installed in single step

Pip::

  pip install cloudsearch-logger

or you can use ``easy_install``

Easy Install::

  easy_install cloudsearch-logger

Manual::

  python setup.py install

Usage
-----
You can use this cloudsearch logger in python scripting code and in django web application as well.

**Example1**

::

  import logging
  import uuid

  from cloudsearch_logger import CloudSearchHandler

  test_logger = logging.getLogger('python-cloudsearch-logger')
  test_logger.setLevel(logging.INFO)
  test_logger.addHandler(CloudSearchHandler(
      domain='domain-name',
      region='us-east-1',
      aws_access_key_id='aws-access-key-id',
      aws_secret_access_key='aws-access-secret-key'))

  data = dict(_document_id=str(uuid.uuid4()), ...)

  test_logger.info(data)

Using with Django
-----------------
Modify your ``settings.py`` file to integrate ``cloudsearch-logger`` with Django's logging::

  LOGGING = {
    ...
    'handlers': {
        'cloudsearch': {
            'level': 'INFO',
            'class': 'cloudsearch_logger.CloudSearchHandler',
            'domain': 'domain-name',
            'region': 'us-east-1',  # Default value: us-east-1
            'aws_secret_access_key': 'aws-access-secret-key',
            'aws_access_key_id': 'aws-access-key-id'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['cloudsearch'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    ...
  }

You can find more examples in the ``example1.py`` and ``example2.py`` files.