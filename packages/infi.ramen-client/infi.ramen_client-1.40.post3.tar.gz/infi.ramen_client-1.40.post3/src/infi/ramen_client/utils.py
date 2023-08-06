import json
import zlib
import logging
import re
import threading
from decimal import Decimal
from datetime import date, datetime
import time
from schematics.exceptions import ValidationError

# Common logger to be used by all classes
logger = logging.getLogger('ramen_client')


def create_queue_reader_and_writer(config):
    """
    Creates a `QueueReader` and runs it in a separate thread.
    Additionally creates a `QueueWriter` assigned to the same queue.
    Returns the reader and the writer.
    """
    from .queue_reader import QueueReader
    from .queue_writer import QueueWriter
    qr = QueueReader(config)
    t = threading.Thread(target=qr.run)
    t.daemon = True
    t.start()
    qw = QueueWriter(config)
    return qr, qw


def dump_json(data):
    """
    Converts the data to JSON, with support for Decimal, date and datetime values.
    """
    def obj_handler(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, datetime):
            return int(time.mktime(obj.timetuple()) * 1000 + obj.microsecond / 1000)
        elif isinstance(obj, date):
            return int(time.mktime(obj.timetuple()) * 1000)
    return json.dumps(data, default=obj_handler, separators=(',', ':'))


def compress(data):
    """
    Compresses data
    """
    return zlib.compress(data)


def validate_name(s):
    """
    Validates that a given string contains only letters, digits, dashes and underscores.
    """
    if not re.match('[a-zA-Z0-9_-]+$', s):
        raise ValidationError('"%s" is invalid - only letters, digits, dashes and underscores allowed' % s)


def validate_version(s):
    """
    Validates that a given string contains only letters, digits, periods, dashes and underscores.
    """
    if not re.match('[a-zA-Z0-9._-]+$', s):
        raise ValidationError('"%s" is invalid - only letters, digits, periods, dashes and underscores allowed' % s)

