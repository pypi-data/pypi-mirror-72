from .queue import DefaultQueue
from .utils import dump_json, compress, validate_name
import six


class QueueWriter(object):
    """
    Handles writing message to an on-disk queue.
    """

    def __init__(self, config):
        """
        Initializer. Expects a `QueueWriterConfig` instance.
        """
        self._queue = DefaultQueue(config)

    def _validate(self, name, value):
        assert value, 'Missing value for %s' % name
        try:
            validate_name(str(value))
        except:
            raise AssertionError('Invalid characters in %s' % name)

    def push(self, category, data_type, data_version, data, reqid=None):
        """
        Pushes a message to the queue.
        """
        # Validation
        self._validate('category', category)
        self._validate('data_type', data_type)
        self._validate('data_version', data_version)
        # Jsonify and compress data
        if isinstance(data, six.text_type):
            data = data.encode('utf-8')
        elif isinstance(data, six.binary_type):
            pass
        else:
            data = dump_json(data).encode('utf-8')
        data = compress(data)
        # Push to queue
        self._queue.push(category, data_type, data_version, data, reqid)

    def queue_size(self):
        """
        Returns the number of messages currently in the queue.
        """
        return len(self._queue)
