# -*- coding: utf-8 -*-

from unittest import TestCase, SkipTest
import os, shutil
import requests
from time import sleep
import threading
import datetime

from infi.ramen_client.config import QueueReaderConfig, QueueWriterConfig
from infi.ramen_client.queue_writer import QueueWriter
from infi.ramen_client.queue_reader import QueueReader, AutheticationError
from infi.ramen_client.utils import create_queue_reader_and_writer
from . import mock_server


SOME_DATA = dict(
    nums=list(range(5)),
    text='hi',
    date=datetime.date.today(),
    datetime=datetime.datetime.now()
)


class QueueReaderTest(TestCase):

    def setUp(self):
        self.config = QueueReaderConfig(dict(
            sender='imx',
            system_serial=1099,
            system_version='3.0.0.1',
            queue_dir='/tmp/ramen_client',
            hostname='127.0.0.1:5000',
            auth_token='good-token',
            ssl=False
        ))
        self.qw = QueueWriter(self.config)
        mock_server.start_server()
        sleep(0.2) # wait for mock server to be ready

    def tearDown(self):
        mock_server.stop_server()
        shutil.rmtree(self.config.queue_dir)

    def test_empty_queue(self):
        qr = QueueReader(self.config)
        r = qr.consume_one()
        self.assertEquals(r, QueueReader.EMPTY)

    def test_success(self):
        self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        qr = QueueReader(self.config)
        r = qr.consume_one()
        self.assertEquals(r, QueueReader.ACCEPTED)

    def test_invalid_token(self):
        self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        self.config.auth_token = 'bad-token'
        qr = QueueReader(self.config)
        with self.assertRaises(AutheticationError):
            r = qr.consume_one()

    def test_invalid_host(self):
        self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        self.config.hostname = 'bad-host-name'
        qr = QueueReader(self.config)
        r = qr.consume_one()
        self.assertEquals(r, QueueReader.RETRY)

    def test_timeout(self):
        self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        self.config.server_timeout = 1
        qr = QueueReader(self.config)
        requests.get('http://127.0.0.1:5000/set_delay?delay=30')
        r = qr.consume_one()
        self.assertEquals(r, QueueReader.RETRY)

    def test_retry(self):
        responses = {
            429: '{"code": "TOO_MANY_REQUESTS", "details": "Rate limit reached"}',
            500: 'Internal Server Error',
            502: 'Bad Gateway',
            503: 'Service Unavailable',
            504: 'Gateway Timeout'
        }
        self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        qr = QueueReader(self.config)
        for status_code, body in responses.items():
            requests.get('http://127.0.0.1:5000/set_response', params=dict(code=status_code, body=body))
            r = qr.consume_one()
            self.assertEquals(r, QueueReader.RETRY)

    def test_invalid_message(self):
        responses = {
            400: '{"code": "BAD_REQUEST", "details": "The payload cannot be processed"}',
            404: '{"code": "NOT_FOUND", "details": "Wrong URL"}',
            413: '{"code": "PAYLOAD_TOO_LARGE", "details": "Payload too large"}',
            415: '{"code": "UNSUPPORTED_MEDIA_TYPE", "details": "Request body is not JSON"}'
        }
        qr = QueueReader(self.config)
        for status_code, body in responses.items():
            requests.get('http://127.0.0.1:5000/set_response', params=dict(code=status_code, body=body))
            self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
            r = qr.consume_one()
            self.assertEquals(r, QueueReader.DROPPED)

    def test_unexpected_response(self):
        self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        qr = QueueReader(self.config)
        requests.get('http://127.0.0.1:5000/set_response', params=dict(code=409, body='Conflict'))
        r = qr.consume_one()
        self.assertEquals(r, QueueReader.DROPPED)

    def test_wrong_config_type(self):
        wrong_config = QueueWriterConfig(dict(
            sender='imx',
            system_serial=1099,
            system_version='3.0.0.1',
            queue_dir='/tmp/ramen_client',
        ))
        with self.assertRaises(AssertionError):
            QueueReader(wrong_config)

    def test_blacklist(self):
        # Simulate a blacklisted response
        body = '{"code": "DROPPED", "details": "Request matches a blacklist rule", "rule": {"system_serial": 1099}}'
        requests.get('http://127.0.0.1:5000/set_response', params=dict(body=body))
        # Check that the next item is dropped
        self.config.blacklist_ttl = 2
        qr = QueueReader(self.config)
        self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        r = qr.consume_one()
        self.assertEquals(r, QueueReader.DROPPED)
        # Reset response to normal
        requests.get('http://127.0.0.1:5000/set_response')
        # The next item should still be dropped by the queue writer
        self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        r = qr.consume_one()
        self.assertEquals(r, QueueReader.DROPPED)
        # After two seconds the blacklist rule should be removed automatically
        sleep(2)
        self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        r = qr.consume_one()
        self.assertEquals(r, QueueReader.ACCEPTED)

    def test_run_loop_blocking(self):
        # Start queue reader loop in separate thread
        self.config.polling_delay = 0.01
        self.config.retry_delay = 0.01
        qr = QueueReader(self.config)
        t = threading.Thread(target=qr.run)
        t.daemon = True
        # Put items in the queue and see that they disappear
        self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        t.start()
        sleep(0.3)
        self.assertEquals(self.qw.queue_size(), 0)
        # Put an item in the queue and see that it remains when retry is required
        requests.get('http://127.0.0.1:5000/set_response',
                     params=dict(code=429, body='{"code": "TOO_MANY_REQUESTS", "details": "Rate limit reached"}'))
        self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        sleep(0.1)
        self.assertEquals(self.qw.queue_size(), 1)
        # Turn off retry, and see that the queue gets drained
        requests.get('http://127.0.0.1:5000/set_response')
        sleep(0.1)
        self.assertEquals(self.qw.queue_size(), 0)

    def test_run_loop_nonblocking(self):
        for i in range(10):
            self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        qr = QueueReader(self.config)
        self.assertEquals(qr.run(blocking=False), 10)
        # Check that the queue is empty
        self.assertEquals(len(self.qw._queue), 0)

    def test_create_queue_reader_and_writer(self):
        self.config.polling_delay = 0.01
        self.config.retry_delay = 0.01
        qr, qw = create_queue_reader_and_writer(self.config)
        # Put items in the queue and see that they disappear
        qw.push('metrics', 'san_totals', 1, SOME_DATA)
        qw.push('metrics', 'san_totals', 1, SOME_DATA)
        qw.push('metrics', 'san_totals', 1, SOME_DATA)
        sleep(0.5)
        self.assertEquals(qw.queue_size(), 0)
        # Stop the reader and see that items remain in the queue
        qr.stop()
        qw.push('metrics', 'san_totals', 1, SOME_DATA)
        sleep(0.1)
        self.assertEquals(qw.queue_size(), 1)
        # Restart the reader
        count = qr.run(blocking=False)
        self.assertEquals(count, 1)
        self.assertEquals(qw.queue_size(), 0)

    def test_proxy_success(self):
        # This test is skipped unless tinyproxy is installed (apt-get install tinyproxy)
        from subprocess import check_output, CalledProcessError
        try:
            check_output('service tinyproxy status', shell=True)
        except CalledProcessError:
            raise SkipTest('tinyproxy is not installed or not running')
        self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        self.config.proxy = 'http://localhost:8888/'
        qr = QueueReader(self.config)
        r = qr.consume_one()
        self.assertEquals(r, QueueReader.ACCEPTED)

    def test_proxy_failure(self):
        # This test ensures that the request actually tries to go through a proxy, and fails
        self.qw.push('metrics', 'san_totals', 1, SOME_DATA)
        self.config.proxy = 'http://localhost:17171/' # no proxy there...
        qr = QueueReader(self.config)
        r = qr.consume_one()
        self.assertEquals(r, QueueReader.RETRY)

    def test_connection_testing_passed(self):
        qr = QueueReader(self.config)
        res = qr.test_connection()
        self.assertTrue(res)

    def test_connection_testing_failed(self):
        self.config.auth_token = 'bad-token'
        qr = QueueReader(self.config)

        res = qr.test_connection()
        self.assertFalse(res)
