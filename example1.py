"""
Created on Oct 8, 2016

@author: ahmadjaved.se@gmail.com

I have created test domain in amazon cloudsearch and made indexes for following
fields:

    appointment_id, facility_id, from_, message_id, message_kind_id,
    message_type_id, patient_id, to, delivery_time

So if we need to use cloudsearch logger in python script then we can use this
logger as given below.
"""
import logging
import uuid
from datetime import datetime

from cloudsearch_logger import CloudSearchHandler

test_logger = logging.getLogger('python-cloudsearch-logger')
test_logger.setLevel(logging.INFO)
test_logger.addHandler(CloudSearchHandler(
    domain='domain-name',
    region='us-east-1',
    aws_access_key_id='aws-access-key-id',
    aws_secret_access_key='aws-access-secret-key'))

data = dict(appointment_id=20, facility_id=20, from_='01010101', message_id=20,
            message_kind_id=1, message_type_id=1, patient_id=20, to='531321',
            delivery_time=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            _document_id=str(uuid.uuid4()))

test_logger.info(data)
