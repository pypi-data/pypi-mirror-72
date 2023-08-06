#
# A mock Ramen server for testing.
#
# To run the server from the commandline:
# FLASK_APP=src/tests/mock_server.py bin/flask run
#

from flask import Flask, request, make_response
from multiprocessing import Process
from time import sleep
import logging


app = Flask(__name__)

default_response_body = '{"code": "ACCEPTED", "details": null}'
default_response_code = 202

delay = 0
response_body = default_response_body
response_code = default_response_code

flask_process = None


def start_server():
    # Runs Flask in a separate process
    global flask_process
    flask_process = Process(target=app.run)
    flask_process.daemon = True
    flask_process.start()


def stop_server():
    # Stops the Flask process
    global flask_process
    if flask_process:
        flask_process.terminate()
        flask_process = None


@app.route('/set_delay')
def set_delay():
    # This API sets the delay in seconds before the mock server returns a response
    global delay
    delay = int(request.args.get('delay', 0))
    return 'OK'


@app.route('/set_response')
def set_reponse():
    # This API sets the status code and body of all future responses
    global response_body
    global response_code
    response_body = request.args.get('body', default_response_body)
    response_code = request.args.get('code', default_response_code)
    return 'OK'


@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def respond(path):
    # Catchall view that performs authentication and then returns the response
    global response_body
    global response_code
    global delay
    if delay:
        sleep(delay)
    if request.headers.get('X-API-Token') != 'good-token':
        return make_response('{"code": "UNAUTHORIZED", "details": "Credentials missing or invalid"}', 401)
    return make_response(response_body, response_code)
