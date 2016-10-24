"""
Created on Oct 8, 2016

@author: ahmadjaved.se@gmail.com

This library is provided to allow standard python logging
to output log data in dictionary format to log it on amazon cloudsearch service.
"""
import datetime
import logging
import re
import traceback
from inspect import istraceback

from cloudsearch_logger import constants

# Support order in python 2.7 and 3
try:
    from collections import OrderedDict
except ImportError:
    pass


class CloudSearchFormatter(logging.Formatter):
    """
    A custom formatter to format logging records as dictionary to log data on
    amazon cloudsearch.
    """

    def __init__(self, *args, **kwargs):
        """
        :param json_handler: a function for encoding non-standard objects
            as outlined in http://docs.python.org/2/library/json.html
        :param datefmt: (optional) a format in which datetime will convert into
            sting format. By default it '%Y-%m-%dT%H:%M:%SZ' because cloudsearch
            allow datetime in this format.
        """
        self.json_handler = kwargs.pop(constants.LABEL_JSON_HANDLER,
                                       self._default_json_handler)
        kwargs[constants.LABEL_DATEFMT] = kwargs.get(
            constants.LABEL_DATEFMT, constants.CLOUDSEARCH_DATETIME_FORMAT)
        logging.Formatter.__init__(self, *args, **kwargs)
        self._fmt_fields = self.get_format_fields()

    def _default_json_handler(self, obj):
        """Format given abject into json formatted string"""
        if isinstance(obj, datetime.datetime):
            if obj.year < 1900:
                # strftime do not work with date < 1900
                return constants.CLOUDSEARCH_DATETIME_CREATION_FORMAT % (
                    obj.year, obj.month, obj.day, obj.hour, obj.minute,
                    obj.second)
            return obj.strftime(self.datefmt)
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.time):
            return obj.strftime(constants.CLOUDSEARCH_TIME_FORMAT)
        elif istraceback(obj):
            _traceback = ''.join(traceback.format_tb(obj))
            return _traceback.strip()
        elif isinstance(obj, Exception):
            return "Exception: %s" % str(obj)
        return str(obj)

    def get_format_fields(self):
        """Get all the required fields mentioned in log message format"""
        _re = re.compile(r'\((.+?)\)', re.IGNORECASE)
        return _re.findall(self._fmt)

    def populate_log_record(self, record, message_dict):
        """
        Populate record's data into python dictionary. Override this method to
        implement custom logic for adding fields.

        :param record: Instance of LogRecord class contains all log information
        :param message_dict: Python dictionary contains log messages information

        :return: Log record in dictionary format
        """
        try:
            log_record = OrderedDict()
        except NameError:
            log_record = {}

        for field in self._fmt_fields:
            log_record[field] = self.json_handler(getattr(record, field, None))
        for field, value in message_dict.iteritems():
            log_record[field] = self.json_handler(value)
        return log_record

    def uses_time(self):
        """
        Check if the format uses the creation time of the record.
        """
        return constants.LABEL_ASCTIME in self._fmt_fields

    def format(self, record):
        """
        Formats a log record and serializes to dictionary with json formatted
        data.

        :param record: Instance of LogRecord class contains all log information

        :return: Log record in dictionary format
        """
        message_dict = {}
        if isinstance(record.msg, dict):
            message_dict = record.msg
            record.message = None

        # only format time when needed
        if self.uses_time():
            record.asctime = self.formatTime(record, self.datefmt)

        # Display formatted exception, but allow overriding it in the
        # user-supplied dict.
        if record.exc_info and not message_dict.get(constants.LABEL_EXC_INFO):
            message_dict[constants.LABEL_EXC_INFO] = self.formatException(
                record.exc_info)

        return self.populate_log_record(record, message_dict)
