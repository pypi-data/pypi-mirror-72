from schematics.models import Model
from schematics.types import StringType, BooleanType, IntType, FloatType
from .utils import validate_name, validate_version


class QueueWriterConfig(Model):
    """
    Configuration parameters for a `QueueWriter` instance.
    """

    # Identifier for the sending program, for example ibox / imx / sa
    sender = StringType(required=True, validators=[validate_name])

    # Serial number of the system
    system_serial = IntType(required=True, min_value=0)

    # Version number of the system
    system_version = StringType(required=True, validators=[validate_version])

    # Directory for storing the queue (multiple systems can use the same directory)
    queue_dir = StringType(default='/var/ramen_client/')

    # Soft limit on the size of the queue in bytes (larger queues will be trimmed)
    max_queue_size = IntType(default=5*1024**3, min_value=10*1024)


class QueueReaderConfig(QueueWriterConfig):
    """
    Configuration parameters for a `QueueReader` instance.
    """

    # Ramen host name
    hostname = StringType(required=True)

    # Authentication token
    auth_token = StringType(required=True)

    # Whether to use HTTPS
    ssl = BooleanType(default=True)

    # The proxy server URL to use
    proxy = StringType(required=False)

    # Connection timeout in seconds
    server_timeout = IntType(default=20, min_value=1, max_value=3600)

    # Number of seconds to wait before checking the queue for new messages
    polling_delay = FloatType(default=5, min_value=0.01, max_value=3600)

    # Number of seconds to wait before trying to resend a failed message
    retry_delay = FloatType(default=30, min_value=0.01, max_value=3600)

    # Number of seconds before rules get removed from the blacklist
    blacklist_ttl = IntType(default=3600, min_value=1, max_value=24*3600)
