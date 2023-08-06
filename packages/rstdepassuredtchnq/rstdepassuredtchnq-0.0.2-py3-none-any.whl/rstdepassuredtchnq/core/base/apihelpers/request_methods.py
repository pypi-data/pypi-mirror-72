import inspect
import requests

from rstdepassuredtchnq.core.base.apihelpers.common_methods import CommonMethods
from rstdepassuredtchnq.core.base.format.pretty_base import PrettyFormat
from rstdepassuredtchnq.core.base.log.custom_logger import get_logger


class BaseAPIHelper:
    pretty_format = PrettyFormat()
    common_data = CommonMethods()
    log = get_logger("BaseAPIHelper")
    USERS_URL = 'http://jsonplaceholder.typicode.com/users'

    def get_request(self, url, params='', auth=None, verify=False):
        resp = None
        self.log.info("post_request")

        try:
            resp = self.get_request_add_auth(url, params, auth=None, verify=False)
            print("*********** - resp.raise_for_status() -> {}".format(resp.raise_for_status()))
            resp.raise_for_status()

        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6

        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')

        # self.common_data.json_viewer(resp)
        assert resp is not None
        return resp

    def post_request_no_header(self, url, data, verify=False, amend_headers=True):
        self.log.info("post_request")
        resp = requests.post(url, data=data, verify=verify)
        # self.common_data.json_viewer(resp)
        assert resp is not None
        return resp

    def put_request_no_header(self, url, data, verify=False, amend_headers=True):
        resp = None
        self.log.info("post_request")
        try:
            resp = requests.put(url, data=data, verify=verify)
            print("*********** - resp.raise_for_status() -> {}".format(resp.raise_for_status()))
            resp.raise_for_status()

        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6

        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')

        # self.common_data.json_viewer(resp)
        assert resp is not None
        return resp

    def post_request(self, url, data, headers={}, verify=False, amend_headers=True):
        self.log.info("post_request")
        header_value = self.default_header(headers={}, amend_headers=True)
        resp = requests.post(url, data=data, headers=header_value, verify=verify)
        self.common_data.json_viewer(resp)
        assert resp is not None
        return resp

    def delete_request(self, url):
        resp = requests.delete(url)
        # self.common_data.json_viewer(resp)
        return resp

    def default_header(self, headers={}, amend_headers=True):
        if amend_headers:
            if not 'Content-Type' in headers:
                headers['Content-Type'] = r'application/json'
                self.log.info(" -------- Headers has Content-Type {} ".format(headers['Content-Type']))

            if not 'User-Agent' in headers:
                headers['User-Agent'] = 'Python Requests'
                self.log.info(" -------- Headers has User-Agent {} ".format(headers['User-Agent']))
        return headers

    def check_status(self, resp, expected_status_code):
        self.log.info(" -------- Checking the Expected Status {} ".format(expected_status_code))
        # This return caller function's name, not this function post.
        caller_func_name = inspect.stack()[1][3]
        if int(resp.status_code) != int(expected_status_code):
            print('%s failed with response code %s.' % (caller_func_name, resp.status_code))
            assert False, 'Failed on Response Code checking'
        else:
            assert True, "Validated Correct Response code"
        self.log.info(" -------- Checking the Actual Status in Response Code {} ".format(resp.status_code))
        return caller_func_name

    def get_request_add_auth(self, url, params='', auth='', verify=False):
        try:
            if auth is None:
                resp = requests.get(url, params, verify=verify)
            else:
                resp = requests.get(url, params, auth=auth, verify=verify)
        except Exception as ex:
            print('requests.get() failed with exception:', str(ex))
            return None

        return resp


