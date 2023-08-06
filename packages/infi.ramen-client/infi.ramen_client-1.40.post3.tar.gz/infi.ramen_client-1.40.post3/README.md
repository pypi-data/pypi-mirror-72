Overview
========
This library is a reference implementation for a client which sends messages to a Ramen server. It implements all the optional features in the [protocol](https://wiki.infinidat.com/display/HOSTDEV/Ramen+Protocol), including:
- Compression
- Automatic retries
- Honoring blacklist rules

The library was tested on Python 2.7 and 3.5.

Usage
=====
To send messages use a `QueueWriter`, which stores the messages in an on-disk queue. Then, use a `QueueReader` to pull messages from the queue and send them to Ramen. The queue reader can run in a separate thread or even a different process.
There's a shortcut method for creating both a writer and a reader (the reader runs in a background thread):

    from infi.ramen_client.utils import create_queue_reader_and_writer
    from infi.ramen_client.config import QueueReaderConfig

    config = QueueReaderConfig(dict(
        sender='imx',
        system_serial=1099,
        system_version='3.0.0.1',
        hostname='ramen.infinidat.com',
        auth_token='my-auth-token',
    ))
    reader, writer = create_queue_reader_and_writer(config)
    writer.push('metrics', 'san_totals', 'v1', my_data)

Data which is passed to the `QueueWriter` gets automatically serialized to JSON and compressed. The serialization includes support for `Decimal`, `date` and `datetime` objects. Alternatively you may serialize the data yourself and pass it as a string.

Advanced Usage
--------------
To create only a `QueueWriter`:

    from infi.ramen_client.queue_writer import QueueWriter
    writer = QueueWriter(config)
    writer.push('metrics', 'san_totals', 'v1', my_data)

To create only a `QueueReader`:

    from infi.ramen_client.queue_reader import QueueReader
    reader = QueueReader(config)
    reader.run(blocking=True)

If `blocking=True`, the `run` method will continue forever, waiting for messages to be pushed to the queue and retrying to send messages that fail due to temporary reasons. Otherwise, it exits when the queue is empty or after a failure, returning the number of messages it processed.

Retries
-------
Requests which failed due to a temporary reason are retried automatically. This means that messages remain in the queue until they are sent successfully. To prevent the disk queue from growing indefinitely, there's a configurable soft limit on its size. When it grows larger than the limit, some of the older messages will be dropped.

The `QueueReader` generates a request id automatically so that the server will know whether it already processed a given message or not. Alternatively you can pass a `reqid` parameter when pushing data to the queue. This may be useful if your code might send duplicate messages in some cases, and you want the server to de-duplicate them. Note that the duplicates identification matches the full URL path, so the `reqid` only needs to be unique in the scope of a specific URL path.

Configuration
-------------
There are separate configuration containers for queue readers and writers.

#### QueueWriterConfig
- **sender** - Identifier for the sending program, for example ibox / imx / sa
- **system_serial** - Serial number of the system
- **system_version** - Version number of the system
- **queue_dir** - Directory for storing the queue (multiple systems can use the same directory) [default: /var/ramen_client/]
- **max_queue_size** - Soft limit on the size of the queue in bytes (larger queues will be trimmed) [default: 5 GiB]


Sending a testing message
-------------------------
The client provide a method to test the connection and the msgs sending to the queue.
It can be done using the following code:
qr = QueueReader(self.config)
res = qr.test_connection()
if the test was passed the test_connection() method would return True.

#### QueueReaderConfig
This is a subclass of `QueueWriterConfig`, so it includes all fields above plus these:
- **hostname** - Ramen host name
- **auth_token** - Authentication token
- **ssl** - Whether to use HTTPS (only used for testing) [default: true]
- **server_timeout** - Connection timeout in seconds [default: 20]
- **polling_delay** - Number of seconds to wait before checking the queue for new messages [default: 5]
- **retry_delay** - Number of seconds to wait before trying to resend a failed message [default: 30]
- **blacklist_ttl** - Number of seconds before rules get removed from the blacklist [default: 3600]

Development
===========

Checking out the code
---------------------
Run the following commands:

    easy_install -U infi.projector
    projector repository clone git@git.infinidat.com:host-internal/infi.ramen_client.git
    cd infi.ramen_client
    projector devenv build

Running Tests
-------------
This command runs the tests:

    bin/nosetests -vx src/tests

To also generate a coverage report in ./cover/index.html use:

    bin/nosetests -vx src/tests --with-coverage --cover-package=infi.ramen_client --cover-html

Releasing a version
-------------------
Use the following commands:

    projector devenv build --use-isolated-python --clean --prefer-final
    projector requirements freeze --with-install-requires --commit-changes --push-changes
    projector version release <VERSION> --pypi-servers=local
