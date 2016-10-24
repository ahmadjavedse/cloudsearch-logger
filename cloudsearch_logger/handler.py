"""
Created on Oct 8, 2016

@author: ahmadjaved.se@gmail.com
"""
import logging
import uuid

import boto

from cloudsearch_logger import constants
from cloudsearch_logger import exceptions
from cloudsearch_logger import formatter

_defaultFormatter = formatter.CloudSearchFormatter()


class CloudSearchHandler(logging.Handler):
    """
    A handler class which log a logging message on amazon cloud search for each
    logging event.
    """

    def __init__(self, domain=None, region=constants.DEFAULT_REGION,
                 aws_access_key_id=None, aws_secret_access_key=None):
        """
        Initialize the handler.

        :param domain: Cloudsearch domain on which this handler should log the
            information.
        :param region: Amazon Cloudsearch region
        :param aws_access_key_id: Amazon aws access key
        :param aws_secret_access_key: Amazon aws secret access key

        ..warning::
            It might raise DomainNotFound exception if domain not found
        """
        assert domain is not None, constants.ERR_MSG_DOMAIN_REQUIRED
        assert region is not None, constants.ERR_MSG_REGION_REQUIRED
        assert aws_access_key_id is not None, constants.ERR_MSG_ACCESS_KEY_REQUIRED
        assert aws_secret_access_key is not None, constants.ERR_MSG_SECRET_KEY_REQUIRED
        logging.Handler.__init__(self)
        self.connection = boto.connect_cloudsearch2(
            region=region, aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key, sign_request=True)
        self.domain = self.connection.lookup(domain)
        if not self.domain:
            raise exceptions.DomainNotFound('Domain not found with name "%s".'
                                            % domain)

    def format(self, record):
        """
        Format the specified record.

        If a formatter is set, use it. Otherwise, use the default formatter
        for the module.
        """
        if self.formatter:
            fmt = self.formatter
        else:
            fmt = _defaultFormatter
        return fmt.format(record)

    def emit(self, record):
        """
        Log record on amazon cloudsearch service.

        ..info::
            To upload message / document on amazon cloud search it will required
            a unique document id. So if someone want to use its own generated
            unique id then pass that in log message with `_document_id` key.
            e.g. test_logger.info({'_document_id': unique-id, ...})
        """
        try:
            document_data = self.format(record)
            _id = document_data.pop(constants.LABEL_DOCUMENT_ID,
                                    str(uuid.uuid4()))
            doc_service = self.domain.get_document_service()
            doc_service.add(_id, document_data)
            doc_service.commit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)
