from future import standard_library
standard_library.install_aliases()
from builtins import object
import os
import sqlite3
from time import sleep
from _thread import get_ident

from .config import QueueWriterConfig
from .utils import logger


class Queue(object):
    """
    Abstract base class for a queue.
    """

    def __init__(self, config):
        """
        Initializer. Expects a `QueueWriterConfig` instance.
        """
        assert isinstance(config, QueueWriterConfig), 'QueueWriterConfig instance is required'
        config.validate()
        self._config = config
        if not os.path.exists(config.queue_dir):
            os.makedirs(config.queue_dir)

    def push(self, category, data_type, data_version, data, reqid=None):
        """
        Pushes a message to the queue.
        """
        raise NotImplementedError()  # pragma: no cover

    def peek(self):
        """
        Gets the first message from the queue, without removing it.
        Returns a dictionary with 4 keys:  "category", "data_type", "data_version", "data".
         """
        raise NotImplementedError()  # pragma: no cover

    def pop(self):
        """
        Gets the first message from the queue, and removes it.
        Returns a dictionary with 4 keys:  "category", "data_type", "data_version", "data".
        """
        raise NotImplementedError()  # pragma: no cover

    def compact(self):
        """
        Compact the queue after one or more items were removed from it.
        Optional operation.
        """
        pass


class DefaultQueue(Queue):

    _create = """
        CREATE TABLE IF NOT EXISTS queue
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            category TEXT NOT NULL,
            data_type TEXT NOT NULL,
            data_version INTEGER NOT NULL,
            reqid TEXT,
            data BLOB NOT NULL
        )
    """
    _count      = 'SELECT COUNT(*) FROM queue'
    _push       = 'INSERT INTO queue (category, data_type, data_version, reqid, data) VALUES (?, ?, ?, ?, ?)'
    _pop_get    = 'SELECT * FROM queue ORDER BY id LIMIT 1'
    _pop_del    = 'DELETE FROM queue WHERE id = ?'
    _page_count = 'PRAGMA page_count'
    _trim       = 'DELETE FROM queue WHERE id < (SELECT MIN(id) + 0.1 * (MAX(id) - MIN(id)) FROM queue)'

    def __init__(self, config):
        """
        Initializer. Expects a `QueueWriterConfig` instance.
        """
        super(DefaultQueue, self).__init__(config)
        self._connection_cache = {}
        filename = '%s_%s.db' % (self._config.sender, self._config.system_serial)
        self._path = os.path.abspath(os.path.join(self._config.queue_dir, filename))
        if not os.path.exists(self._path):
            self._init_database()

    def _init_database(self):
        """
        Creates and configures the sqlite database.
        """
        with self._get_conn() as conn:
            conn.execute('PRAGMA page_size=4096')
            conn.execute('PRAGMA auto_vacuum=INCREMENTAL')
            conn.execute('PRAGMA journal_mode=WAL')
            conn.execute(self._create)

    def __len__(self):
        """
        Returns the number of messages currently in the queue.
        """
        with self._get_conn() as conn:
            return conn.execute(self._count).fetchone()[0]

    def _get_conn(self):
        """
        Returns a connection to the database. This can be
        called multiple times and the same connection will be returned
        per thread.
        """
        id = get_ident()
        if id not in self._connection_cache:
            conn = sqlite3.Connection(self._path, timeout=60)
            conn.row_factory = sqlite3.Row
            self._connection_cache[id] = conn
        return self._connection_cache[id]

    def push(self, category, data_type, data_version, data, reqid=None):
        """
        Pushes a message to the queue.
        """
        with self._get_conn() as conn:
            conn.execute(self._push, (category, data_type, data_version, reqid, sqlite3.Binary(data)))
            self._enforce_size(conn)

    def peek(self):
        """
        Gets the first message from the queue, without removing it.
        Returns a dictionary with 4 keys:  "category", "data_type", "data_version", "data".
         """
        with self._get_conn() as conn:
            cursor = conn.execute(self._pop_get)
            return cursor.fetchone()

    def pop(self):
        """
        Gets the first message from the queue, and removes it.
        Returns a dictionary with 4 keys:  "category", "data_type", "data_version", "data".
        """
        with self._get_conn() as conn:
            cursor = conn.execute(self._pop_get)
            row = cursor.fetchone()
            if row:
                conn.execute(self._pop_del, (row[0],))
                return row
        return None

    def compact(self):
        """
        Compact the database.
        """
        with self._get_conn() as conn:
            conn.commit()
            conn.execute('VACUUM')

    def _enforce_size(self, conn):
        """
        When the database grows beyond max_queue_size, drop 10% of the oldest rows.
        """
        if self._size_exceeded():
            # Vacuum the database and check if it's still too large
            self.compact()
            if self._size_exceeded():
                # Drop the oldest messages
                logger.warning('Dropping 10%% of the queue because it is larger than the maximum of %d bytes',
                               self._config.max_queue_size)
                conn.execute(self._trim)
                self.compact()

    def _size_exceeded(self):
        """
        Check if the database file is larger than max_queue_size.
        """
        with self._get_conn() as conn:
            size = 4096 * conn.execute(self._page_count).fetchone()[0]
        return size > self._config.max_queue_size
