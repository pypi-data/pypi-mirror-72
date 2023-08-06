import time
from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World'


@app.route('/json', methods=['POST', 'GET'])
def test_json():
    time.sleep(0.2)  # simulate delay
    return '{"code": 1, "message": "Hello, World!" }'


@app.route('/request_headers')
def test_req_headers():
    headers = request.headers

    # Get header values
    # get(key, default=None, type=None, as_bytes=False)
    # Return None if not found
    user_agent = headers.get('User-Agent')
    if user_agent is not None:
        return 'Header User-Agent in the request is %s.' % user_agent
    else:
        return 'Header User-Agent does not exist in the request.'


@app.route('/request_body', methods=['POST', 'GET'])
def test_req_body():
    # get_data(cache=True, as_text=False, parse_form_data=False)
    request_body = request.get_data()
    request_body = request_body.decode('utf-8')  # decode if it is byte string b''
    return 'Request body content is\n%s' % request_body

    # Output for request with '{"key1":"value1","key2":2}':
    # Request body content is b'{"key1":"value1","key2":2}'


# Run in HTTP
app.run(host='127.0.0.1', port='5000')
