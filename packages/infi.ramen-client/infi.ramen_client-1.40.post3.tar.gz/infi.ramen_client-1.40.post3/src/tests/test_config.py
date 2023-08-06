# -*- coding: utf-8 -*-

from unittest import TestCase

from infi.ramen_client.config import QueueReaderConfig, QueueWriterConfig
from schematics.exceptions import ValidationError, DataError



class QueueWriterConfigTest(TestCase):

    def setUp(self):
        self.config = QueueWriterConfig(dict(
            sender='imx',
            system_serial=1099,
            system_version='3.0.0.1'
        ))

    def assertInvalid(self, key, value):
        print('%s=%s' % (key, value))
        prev_value = getattr(self.config, key)
        setattr(self.config, key, value)
        with self.assertRaises((ValidationError, DataError)):
            self.config.validate()
        setattr(self.config, key, prev_value)

    def test_sender(self):
        for value in (None, '', 'with blanks', 'd.o.t.s.', u'פאלי'):
            self.assertInvalid('sender', value)

    def test_system_serial(self):
        for value in (None, '', -100):
            self.assertInvalid('system_serial', value)

    def test_system_version(self):
        for value in (None, '', ' ', u'פאלי'):
            self.assertInvalid('system_version', value)

    def test_max_queue_size(self):
        for value in ('', -100, 2):
            self.assertInvalid('max_queue_size', value)


class QueueReaderConfigTest(QueueWriterConfigTest):

    def setUp(self):
        self.config = QueueReaderConfig(dict(
            sender='imx',
            system_serial=1099,
            system_version='3.0.0.1',
            hostname='127.0.0.1:5000',
            auth_token='good-token'
        ))

    def test_server_timeout(self):
        for value in ('', -100, 20000):
            self.assertInvalid('server_timeout', value)

    def test_polling_delay(self):
        for value in ('', -100, 20000):
            self.assertInvalid('polling_delay', value)

    def test_retry_delay(self):
        for value in ('', -100, 20000):
            self.assertInvalid('retry_delay', value)

