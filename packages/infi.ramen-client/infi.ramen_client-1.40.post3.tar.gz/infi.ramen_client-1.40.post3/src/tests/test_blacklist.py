# -*- coding: utf-8 -*-

from unittest import TestCase

from infi.ramen_client.config import QueueReaderConfig
from infi.ramen_client.queue_reader import Blacklist


class BlacklistTest(TestCase):

    def setUp(self):
        config = QueueReaderConfig(dict(
            sender='imx',
            system_serial=1099,
            system_version='3.0.0.1',
            hostname='127.0.0.1:5000',
            auth_token='good-token'
        ))
        self.bl = Blacklist(config)

    def _matches(self, category='metrics', data_type='san_totals', data_version='v1'):
        item = dict(category=category, data_type=data_type, data_version=data_version)
        return self.bl.matches(item)

    def test_category(self):
        self.bl.add(dict(category='events'))
        self.assertFalse(self._matches())
        self.bl.add(dict(category='metrics'))
        self.assertTrue(self._matches())

    def test_system_serial(self):
        self.bl.add(dict(system_serial=1098))
        self.assertFalse(self._matches())
        self.bl.add(dict(system_serial=1099))
        self.assertTrue(self._matches())

    def test_sender(self):
        self.bl.add(dict(sender='ibox'))
        self.assertFalse(self._matches())
        self.bl.add(dict(sender='imx'))
        self.assertTrue(self._matches())

    def test_data_type(self):
        self.bl.add(dict(data_type='nas_totals'))
        self.assertFalse(self._matches())
        self.bl.add(dict(data_type='san_totals'))
        self.assertTrue(self._matches())

    def test_data_version(self):
        self.bl.add(dict(data_version='v2'))
        self.assertFalse(self._matches())
        self.bl.add(dict(data_version='v1'))
        self.assertTrue(self._matches())

    def test_system_version(self):
        self.bl.add(dict(system_version='4.0.0.1'))
        self.assertFalse(self._matches())
        self.bl.add(dict(system_version='3.0.0.1'))
        self.assertTrue(self._matches())

    def test_double_match(self):
        self.bl.add(dict(system_serial=1099, category='events'))
        self.bl.add(dict(system_serial=1098, category='metrics'))
        self.assertFalse(self._matches())
        self.bl.add(dict(system_serial=1099, category='metrics'))
        self.assertTrue(self._matches())

    def test_full_match(self):
        self.bl.add(dict(system_serial=1098, category='metrics', sender='imx',
                         data_type='san_totals', data_version='v1', system_version='3.0.0.1'))
        self.bl.add(dict(system_serial=1099, category='events', sender='imx',
                         data_type='san_totals', data_version='v1', system_version='3.0.0.1'))
        self.bl.add(dict(system_serial=1099, category='metrics', sender='ibox',
                         data_type='san_totals', data_version='v1', system_version='3.0.0.1'))
        self.bl.add(dict(system_serial=1099, category='metrics', sender='imx',
                         data_type='nas_totals', data_version='v1', system_version='3.0.0.1'))
        self.bl.add(dict(system_serial=1099, category='metrics', sender='imx',
                         data_type='san_totals', data_version='v2', system_version='3.0.0.1'))
        self.bl.add(dict(system_serial=1099, category='metrics', sender='imx',
                         data_type='san_totals', data_version='v1', system_version='4.0.0.1'))
        self.assertFalse(self._matches())
        self.bl.add(dict(system_serial=1099, category='metrics', sender='imx',
                         data_type='san_totals', data_version='v1', system_version='3.0.0.1'))
        self.assertTrue(self._matches())

