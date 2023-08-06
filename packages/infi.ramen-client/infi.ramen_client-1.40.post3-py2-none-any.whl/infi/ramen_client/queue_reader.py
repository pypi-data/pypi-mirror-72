from .config import QueueReaderConfig
from .queue import DefaultQueue
from .utils import dump_json, compress, logger

from schematics.models import Model
from schematics.types import StringType, IntType, DateTimeType
from datetime import datetime, timedelta
from time import sleep
import requests
import socket
import threading
from logging import INFO, WARNING
import uuid


class AutheticationError(Exception):
    """
    Raised by `QueueReader` when it cannot authenticate against the server.
    """
    pass


class QueueReader(object):
    """
    Reads messages from an on-disk queue and sends them to the Ramen server.
    """

    # Status Codes
    EMPTY    = 0 # Queue is empty
    ACCEPTED = 1 # Message was accepted by the server
    DROPPED  = 2 # Message was dropped by the server or the blacklist
    RETRY    = 3 # Try to resend the message later

    def __init__(self, config):
        """
        Initializer. Expects a `QueueReaderConfig` instance.
        """
        assert isinstance(config, QueueReaderConfig), 'QueueReaderConfig instance is required'
        config.validate()
        self._config = config
        self._queue = DefaultQueue(config)
        self._blacklist = Blacklist(config)
        self._session = requests.Session()
        self._session.proxies = self._proxies()
        self._session.headers.update({
            'X-API-Token': config.auth_token,
            'Content-Type': 'application/json',
            'Content-Encoding': 'gzip'
        })
        self._stop_event = threading.Event()

    def _proxies(self):
        """
        Returns a dictionary of proxies for requests.
        """
        proxy = self._config.proxy
        return dict(http=proxy, https=proxy) if proxy else {}

    def run(self, blocking=True):
        """
        Reads messages from the queue and sends them to the Ramen server.
        Raises `AutheticationError` if the credentials are wrong.
        If `blocking=True`, this method will run forever, waiting for
        messages to be pushed to the queue and retrying to send messages
        that fail due to temporary reasons. Otherwise, it exits when the
        queue is empty, returning the number of messages it processed.
        """
        count = 0
        self._stop_event.clear() # in case stop was called previously
        while not self._stop_event.is_set():
            result = self.consume_one()
            if result == self.EMPTY:
                if count:
                    self._queue.compact()
                if not blocking:
                    break
                self._stop_event.wait(self._config.polling_delay)
            elif result == self.RETRY:
                if not blocking:
                    break
                self._stop_event.wait(self._config.retry_delay)
            else:
                count += 1
        return count

    def stop(self):
        """
        When running the reader in a background thread, use this method
        to stop and terminate the thread.
        """
        self._stop_event.set()

    def consume_one(self):
        """
        Attempts to handle one message from the queue.
        Returns EMPTY, ACCEPTED, DROPPED or RETRY.
        Raises `AutheticationError` if the credentials are wrong.
        """
        item = self._queue.peek()
        if item is None:
            # Queue is empty
            result = self.EMPTY
        elif self._blacklist.matches(item):
            # Blacklisted item, do not send to server
            result = self.DROPPED
        else:
            # Send to the server
            result = self._send(item)
        # Remove item from queue if it was accepted or dropped
        if result in (self.ACCEPTED, self.DROPPED):
            self._queue.pop()
        return result

    def _send(self, item):
        """
        Sends one message to the server and returns ACCEPTED, DROPPED or RETRY.
        Raises `AutheticationError` if the credentials are wrong.
        """
        url = self._build_url(item)
        logger.info('POST %s', url)
        try:
            r = self._session.post(url, item['data'], timeout=self._config.server_timeout)
            logger.log(INFO if r.status_code == 202 else WARNING,
                       'HTTP %d %s', r.status_code, r.text or '')
            if r.status_code == 429 or r.status_code >= 500:
                # Rate limiting or server-side problem
                return self.RETRY
            if r.status_code in (400, 404, 413, 415):
                # Something's wrong with the message
                return self.DROPPED
            if r.status_code in (401, 403):
                # Wrong credentials
                raise AutheticationError('%(code)s - %(details)s', r.json())
            if r.status_code != 202:
                # Unexpected response
                return self.DROPPED
            j = r.json()
            if j['code'] == 'DROPPED':
                self._blacklist.add(j['rule'])
                return self.DROPPED
            else:
                return self.ACCEPTED
        except requests.ConnectionError as e:
            logger.exception('Connection error on %s', url)
            return self.RETRY
        except requests.Timeout:
            logger.exception('Timeout on %s', url)
            return self.RETRY

    def _build_url(self, item):
        url = '{protocol}://{host}/ramen/v1/{category}/{serial}/{sender}.{data_type}.{data_ver}/?version={system_ver}&reqid={reqid}'
        params = dict(
            protocol='https' if self._config.ssl else 'http',
            host=self._config.hostname,
            category=item['category'],
            serial=self._config.system_serial,
            sender=self._config.sender,
            data_type=item['data_type'],
            data_ver=item['data_version'],
            system_ver=self._config.system_version,
            reqid=item['reqid'] or item['id']
        )
        return url.format(**params)


    def test_connection(self):
        try:
            fake_item = dict(
                category="metrics",
                data_type="test",
                data_version="v1",
                reqid=str(uuid.uuid4().hex),
                data='{}'
            )
            test_results = self._send(item=fake_item)
            return test_results == self.ACCEPTED
        except AutheticationError:
            return False

    def get_blacklist(self):
        return self._blacklist.get_list()




class Blacklist(object):
    """
    Encapsulates blacklisting of messages. Keeps a list of blacklist rules and checks
    whether any of them match a given message. Rules have a fixed TTL (time to live)
    before being removed.
    """

    class Rule(Model):
        """
        Encapsulates a blacklist rule. A rule matches a given message when
        all non-empty rule parameters equal the relevant fields in the message
        and/or configuration.
        """
        added = DateTimeType(default=datetime.now)
        last_seen = DateTimeType(default=datetime.now)
        category = StringType()
        system_serial = IntType()
        sender = StringType()
        data_type = StringType()
        data_version = StringType()
        system_version = StringType()

        def __str__(self):
            fields = []
            for field in ('category', 'system_serial', 'sender', 'data_type', 'data_version', 'system_version'):
                if self[field]:
                    fields.append('%s=%s' % (field, self[field]))
            return 'Rule(' + ', '.join(fields) + ')'

    def __init__(self, config):
        """
        Initializer. Expects a `QueueReaderConfig` instance.
        """
        self._config = config
        self._rules = []

    def add(self, rule_fields):
        """
        Adds a rule to the blacklist.
        """
        self._rules.append(Blacklist.Rule(rule_fields))

    def matches(self, item):
        """
        Returns `True` if any of the rules in the blacklist match the given message.
        """
        result = False
        if self._rules:
            expiry_time = datetime.now() - timedelta(seconds=self._config.blacklist_ttl)
            expired_rules = []
            # Check all rules
            for rule in self._rules:
                if rule.last_seen < expiry_time:
                    # The rule is expired
                    expired_rules.append(rule)
                else:
                    # Check the rule
                    result |= self.check_match(rule, item)
            # Remove expired rules
            for rule in expired_rules:
                self._rules.remove(rule)
        return result

    def check_match(self, rule, item):
        """
        Returns `True` if the given rule and message match.
        """
        return all([
            rule.category       is None or rule.category        == item['category'],
            rule.system_serial  is None or rule.system_serial   == self._config.system_serial,
            rule.sender         is None or rule.sender          == self._config.sender,
            rule.data_type      is None or rule.data_type       == item['data_type'],
            rule.data_version   is None or rule.data_version    == item['data_version'],
            rule.system_version is None or rule.system_version  == self._config.system_version
        ])

    def get_list(self):
        return self._rules