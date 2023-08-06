# -*- coding: utf-8 -*-

from unittest import TestCase
import os, shutil
import json
import zlib
from datetime import date, datetime
from decimal import Decimal
from schematics.exceptions import ValidationError

from infi.ramen_client.config import QueueWriterConfig
from infi.ramen_client.queue_writer import QueueWriter


def decode(buf):
    return json.loads(zlib.decompress(buf).decode('utf-8'))


class QueueWriterTest(TestCase):

    def setUp(self):
        self.config = QueueWriterConfig(dict(
            sender='imx',
            system_serial=1099,
            system_version='3.0.0.1',
            queue_dir='/tmp/ramen_client',
        ))
        self.qw = QueueWriter(self.config)

    def tearDown(self):
        shutil.rmtree(self.config.queue_dir)

    def test_push_list(self):
        self.qw.push('metrics', 'san_totals', 1, list(range(5)))
        self.qw.push('metrics', 'nas_totals', 2, list(range(10)), reqid='123')
        self.assertEquals(self.qw.queue_size(), 2)
        item = self.qw._queue.pop()
        self.assertEquals(item['category'], 'metrics')
        self.assertEquals(item['data_type'], 'san_totals')
        self.assertEquals(item['data_version'], 1)
        self.assertEquals(item['reqid'], None)
        self.assertEquals(decode(item['data']), list(range(5)))
        item = self.qw._queue.pop()
        self.assertEquals(item['category'], 'metrics')
        self.assertEquals(item['data_type'], 'nas_totals')
        self.assertEquals(item['data_version'], 2)
        self.assertEquals(item['reqid'], '123')
        self.assertEquals(decode(item['data']), list(range(10)))
        item = self.qw._queue.pop()
        self.assertEquals(item, None)

    def test_push_dict(self):
        data = dict(a=1, b=list(range(5)), c=u'שלום',
                    d=datetime.now().replace(microsecond=17000), e=date.today(), f=Decimal(3.14))
        self.qw.push('metrics', 'san_totals', 1, data)
        item = self.qw._queue.pop()
        self.assertEquals(item['category'], 'metrics')
        self.assertEquals(item['data_type'], 'san_totals')
        self.assertEquals(item['data_version'], 1)
        result = decode(item['data'])
        print(result)
        self.assertEquals(result['a'], data['a'])
        self.assertEquals(result['b'], data['b'])
        self.assertEquals(result['c'], data['c'])
        self.assertEquals(datetime.fromtimestamp(result['d'] / 1000.0), data['d']) # datetimes are converted to timestamps in millis
        self.assertEquals(date.fromtimestamp(result['e'] / 1000.0), data['e']) # dates are converted to timestamps in millis
        self.assertEquals(result['f'], float(data['f'])) # decimals are converted to floats

    def test_push_string(self):
        data = json.dumps(dict(a=1, b=list(range(5))))
        for s in (data, data.encode('utf-8')):
            self.qw.push('metrics', 'san_totals', 1, data)
            item = self.qw._queue.pop()
            self.assertEquals(item['category'], 'metrics')
            self.assertEquals(item['data_type'], 'san_totals')
            self.assertEquals(item['data_version'], 1)
            self.assertEquals(decode(item['data']), dict(a=1, b=list(range(5))))

    def test_push_large(self):
        self.qw.push('metrics', 'san_totals', 1, list(range(1000000)))
        item = self.qw._queue.pop()
        self.assertEquals(decode(item['data']), list(range(1000000)))

    def test_queue_size_not_exceeded(self):
        # Push 250 items without exceeding max_queue_size, make sure they are all there
        data = list(range(1000))
        for i in list(range(250)):
            self.qw.push('metrics', 'san_totals', 1, data)
        self.assertEquals(self.qw.queue_size(), 250)

    def test_queue_size_exceeded(self):
        # Push 250 items that exceed max_queue_size, make sure some were dropped
        self.config.max_queue_size = 10240
        qw = QueueWriter(self.config)
        data = list(range(1000))
        for i in list(range(250)):
            qw.push('metrics', 'san_totals', 1, data)
        self.assertTrue(len(qw._queue) < 250)

    def test_invalid_category(self):
        for category in (None, '', ' ', 'a.b.c', '/', '\\'):
            with self.assertRaises(AssertionError):
                self.qw.push(category, 'san_totals', 1, '')

    def test_invalid_data_type(self):
        for data_type in (None, '', ' ', 'a.b.c', '/', '\\'):
            with self.assertRaises(AssertionError):
                self.qw.push('metrics', data_type, 1, '')

    def test_invalid_data_version(self):
        for data_version in (None, '', ' ', 'a.b.c', '/', '\\'):
            with self.assertRaises(AssertionError):
                self.qw.push('metrics', 'san_totals', data_version, '')

    def test_vacuum(self):
        # Put data in the queue and get its size
        data = list(range(10000))
        for i in list(range(101)):
            self.qw.push('metrics', 'san_totals', 1, data)
        # The 100th pop should trigger vacuuming
        for i in list(range(101)):
            self.qw._queue.pop()
        # There's no easy way to validate that vacuuming worked, but coverage will show that it ran.
