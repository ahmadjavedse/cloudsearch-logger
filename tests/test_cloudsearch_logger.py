"""
Created on Oct 23, 2016

@author: ahmadjaved.se@gmail.com

Tests to validate the functionality of `CloudSearchFormatter` and
`CloudSearchHandler` classes. These are mocked tests, these tests will not make
any request with amazon cloudsearch server.
"""
import logging
import sys
import unittest
import uuid
from datetime import datetime

from mock import patch
from testscenarios.testcase import TestWithScenarios

from cloudsearch_logger import CloudSearchFormatter
from cloudsearch_logger import CloudSearchHandler
from cloudsearch_logger import constants
from cloudsearch_logger import exceptions

NOW = datetime.now()


class MockDocumentService(object):
    def __init__(self):
        pass

    def add(self, _id, fields):
        pass

    def commit(self):
        pass


class MockDomain(object):
    def __init__(self):
        pass

    def get_document_service(self):
        return MockDocumentService()


class MockLayer2(object):
    def __init__(self):
        pass

    def lookup(self, domain):
        return MockDomain()


def generate_traceback_obj():
    try:
        1 / 0
    except Exception as e:
        return sys.exc_info()[2]


class CloudSearchLoggerTests(TestWithScenarios):
    scenarios = [
        ('Scenario 1', dict(
            boto_credentials=dict(
                domain='domain-name', region='us-east-2',
                aws_access_key_id='aws-access-key-id',
                aws_secret_access_key='aws-access-secret-key'),
            log_data=dict(
                appointment_id=1, facility_id=1, from_='01010101', message_id=1,
                message_kind_id=1, message_type_id=1, patient_id=1, to='531321',
                delivery_time=NOW,
                _document_id=str(uuid.uuid4())),
            expected_connection_params=dict(
                sign_request=True, region='us-east-2',
                aws_access_key_id='aws-access-key-id',
                aws_secret_access_key='aws-access-secret-key'),
            expected_added_document_data=dict(
                delivery_time=NOW.strftime(
                    constants.CLOUDSEARCH_DATETIME_FORMAT),
                from_='01010101', patient_id='1', to='531321', facility_id='1',
                appointment_id='1', message_kind_id='1', message='None',
                message_id='1', message_type_id='1')
        )),
        ('Scenario 2', dict(
            boto_credentials=dict(
                domain='domain-name', aws_access_key_id='aws-access-key-id',
                aws_secret_access_key='aws-access-secret-key'),
            log_data=dict(
                appointment_id=1, facility_id=1, from_='01010101', message_id=1,
                message_kind_id=1, message_type_id=1, patient_id=1, to='531321',
                delivery_time=NOW.strftime(
                    constants.CLOUDSEARCH_DATETIME_FORMAT)),
            expected_connection_params=dict(
                sign_request=True, region='us-east-1',
                aws_access_key_id='aws-access-key-id',
                aws_secret_access_key='aws-access-secret-key'),
            expected_added_document_data=dict(
                delivery_time=NOW.strftime(
                    constants.CLOUDSEARCH_DATETIME_FORMAT),
                from_='01010101', patient_id='1', to='531321', facility_id='1',
                appointment_id='1', message_kind_id='1', message='None',
                message_id='1', message_type_id='1')
        )),
        ('Scenario 3', dict(
            boto_credentials=dict(
                domain='domain-name', aws_access_key_id='aws-access-key-id',
                aws_secret_access_key='aws-access-secret-key'),
            log_data=dict(
                appointment_id=1, facility_id=1, from_='01010101', message_id=1,
                message_kind_id=1, message_type_id=1, patient_id=1, to='531321',
                delivery_time=NOW.replace(year=1880),
                delivery_date=NOW.replace(year=1880).date(),
                delivery_time_only=NOW.replace(year=1880).time(),
                exce_info=Exception('Testing'), trace=generate_traceback_obj()),
            expected_connection_params=dict(
                sign_request=True, region='us-east-1',
                aws_access_key_id='aws-access-key-id',
                aws_secret_access_key='aws-access-secret-key'),
            expected_added_document_data=dict(
                delivery_time='1880%s' % NOW.strftime(
                    constants.CLOUDSEARCH_DATETIME_FORMAT)[4:],
                from_='01010101', patient_id='1', to='531321', facility_id='1',
                appointment_id='1', message_kind_id='1', message='None',
                message_id='1', message_type_id='1',
                delivery_date=NOW.replace(year=1880).date().isoformat(),
                delivery_time_only=NOW.replace(year=1880).time().strftime(
                    constants.CLOUDSEARCH_TIME_FORMAT),
                exce_info='Exception: Testing')
        )),
    ]

    def setUp(self):
        self.test_logger = logging.getLogger('python-cloudsearch-logger')
        self.test_logger.setLevel(logging.INFO)

    def test_default_formatter(self):
        with patch('boto.connect_cloudsearch2') as mock_connect_cloudsearch2, \
                patch.object(MockDocumentService, 'add') as mock_add, \
                patch.object(MockDocumentService, 'commit') as mock_commit:
            mock_connect_cloudsearch2.return_value = MockLayer2()
            self.test_logger.addHandler(CloudSearchHandler(
                **self.boto_credentials))
            self.test_logger.info(self.log_data)

        self.assertTrue(mock_connect_cloudsearch2.called)
        for key, value in self.expected_connection_params.iteritems():
            called_values = mock_connect_cloudsearch2.call_args[1]
            self.assertEqual(called_values[key], value)

        self.assertTrue(mock_add.called)
        if '_document_id' in self.log_data:
            self.assertEqual(mock_add.call_args[0][0],
                             self.log_data['_document_id'])
        else:
            self.assertIsInstance(mock_add.call_args[0][0], str)
            self.assertGreater(len(mock_add.call_args[0][0]), 0)
        for key, value in self.expected_added_document_data.iteritems():
            formatted_document_data = mock_add.call_args[0][1]
            self.assertEqual(formatted_document_data[key], value)

        self.assertTrue(mock_commit.called)

    def test_custom_formatter(self):
        with patch('boto.connect_cloudsearch2') as mock_connect_cloudsearch2, \
                patch.object(MockDocumentService, 'add') as mock_add, \
                patch.object(MockDocumentService, 'commit') as mock_commit:
            mock_connect_cloudsearch2.return_value = MockLayer2()
            formatter = CloudSearchFormatter(fmt='%(message)s %(asctime)s')
            handler = CloudSearchHandler(**self.boto_credentials)
            handler.setFormatter(formatter)
            self.test_logger.addHandler(handler)
            self.test_logger.info(self.log_data)

        self.assertTrue(mock_connect_cloudsearch2.called)
        for key, value in self.expected_connection_params.iteritems():
            called_values = mock_connect_cloudsearch2.call_args[1]
            self.assertEqual(called_values[key], value)

        self.assertTrue(mock_add.called)
        if '_document_id' in self.log_data:
            self.assertEqual(mock_add.call_args[0][0],
                             self.log_data['_document_id'])
        else:
            self.assertIsInstance(mock_add.call_args[0][0], str)
            self.assertGreater(len(mock_add.call_args[0][0]), 0)
        for key, value in self.expected_added_document_data.iteritems():
            formatted_document_data = mock_add.call_args[0][1]
            self.assertEqual(formatted_document_data[key], value)

        self.assertTrue(mock_commit.called)


class ErrorHandlingTests(unittest.TestCase):
    def setUp(self):
        self.boto_credentials = dict(
            domain='domain-name', region='us-east-1',
            aws_access_key_id='aws-access-key-id',
            aws_secret_access_key='aws-access-secret-key')
        self.log_data = dict(
            appointment_id=1, facility_id=1, from_='01010101', message_id=1,
            message_kind_id=1, message_type_id=1, patient_id=1, to='531321',
            delivery_time=NOW, _document_id=str(uuid.uuid4()))
        self.test_logger = logging.getLogger('python-cloudsearch-logger')
        self.test_logger.setLevel(logging.INFO)

    def test_domain_not_found_handling(self):
        with patch('boto.connect_cloudsearch2') as mock_connect_cloudsearch2:
            with patch.object(MockLayer2, 'lookup') as mock_lookup:
                mock_connect_cloudsearch2.return_value = MockLayer2()
                mock_lookup.return_value = None
                with self.assertRaises(exceptions.DomainNotFound) as context:
                    handler = CloudSearchHandler(**self.boto_credentials)

        self.assertTrue(mock_connect_cloudsearch2.called)
        self.assertEqual(context.exception.message,
                         'Domain not found with name "%s".' %
                         self.boto_credentials['domain'])

    def test_keyboard_interrupt_error_handling(self):
        with patch('boto.connect_cloudsearch2') as mock_connect_cloudsearch2:
            with patch.object(MockDocumentService, 'add') as mock_add:
                mock_connect_cloudsearch2.return_value = MockLayer2()
                mock_add.side_effect = KeyboardInterrupt()
                self.test_logger.addHandler(CloudSearchHandler(
                    **self.boto_credentials))
                with self.assertRaises(KeyboardInterrupt) as context:
                    self.test_logger.info(self.log_data)

        self.assertTrue(mock_connect_cloudsearch2.called)

    def test_exception_error_handling(self):
        with patch('boto.connect_cloudsearch2') as mock_connect_cloudsearch2, \
                patch.object(MockDocumentService, 'add') as mock_add, \
                patch.object(CloudSearchHandler,
                             'handleError') as mock_handle_error:
            mock_connect_cloudsearch2.return_value = MockLayer2()
            mock_add.side_effect = Exception('Testing')
            self.test_logger.addHandler(CloudSearchHandler(
                **self.boto_credentials))
            self.test_logger.info(self.log_data)

        self.assertTrue(mock_connect_cloudsearch2.called)
        self.assertTrue(mock_handle_error.called)


if __name__ == '__main__':
    unittest.main()
