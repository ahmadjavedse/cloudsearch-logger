"""
Created on Oct 23, 2016

@author: ahmadjaved.se@gmail.com

This example shows how to setup cloudsearch logger using logging dict config.

Please see the doc string of example1 as well.
"""
import logging.config
import uuid
from datetime import datetime

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'cloudsearch': {
            '()': 'cloudsearch_logger.CloudSearchFormatter',
            'format': ('%(message)s')
        }
    },
    'handlers': {
        'cloudsearch': {
            'level': 'INFO',
            'class': 'cloudsearch_logger.CloudSearchHandler',
            'domain': 'domain-name',
            'region': 'us-east-1',
            'aws_secret_access_key': 'aws-access-secret-key',
            'aws_access_key_id': 'aws-access-key-id',
            'formatter': 'cloudsearch'
        }
    },
    'loggers': {
        'cloudsearch_logger': {
            'handlers': ['cloudsearch'],
            'propagate': False,
            'level': 'INFO'
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
cloudsearch_logger = logging.getLogger('cloudsearch_logger')

data = dict(appointment_id=10, facility_id=10, from_='01010101', message_id=10,
            message_kind_id=1, message_type_id=1, patient_id=10, to='531321',
            delivery_time=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            _document_id=str(uuid.uuid4()))

cloudsearch_logger.info(data)
