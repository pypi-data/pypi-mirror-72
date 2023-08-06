import inspect
import json
import os
from selenium.webdriver.remote.utils import load_json

# This is just for demo
from rstdepassuredtchnq.core.base.format.pretty_base import PrettyFormat
from rstdepassuredtchnq.core.base.log.custom_logger import get_logger


class CommonMethods:
    pretty_format = PrettyFormat()
    log = get_logger("CommonMethods")

    def read_payload(self, log_dir, file_name):
        file = open('%s/%s' % (log_dir, file_name), )
        request_json = json.load(file)
        self.log.info(" Requesting Payload in Put Request {} ".format(request_json))
        return request_json

    def load_json(self, resp):
        json_resp = json.load(resp)
        print("**** json_resp {} ".format(json_resp))
        return json_resp

    def fetch_json(self, resp, value):
        json_text = load_json(resp)
        print('Actual Response in Json Text is %s ' % json_text)
        actual_value = json_text[value]
        print('Actual value in Json Text is %s ' % actual_value)
        return actual_value

    def fetch_json_subnode(self, resp):
        json_text = load_json(resp)
        return json_text

    def parse_from_response(self, json_response, value):
        parse_value = json_response[value]
        print('Actual value in Json Text is %s ' % parse_value)
        return parse_value

    def parse_subnode_from_response(self, json_response, value, value2):
        parse_value = json_response[value][value2]
        print('Actual value in Json Text is %s ' % parse_value)
        return parse_value

    def json_viewer(self, resp):
        self.pretty_format.pretty_print_request(resp.request)
        self.pretty_format.pretty_print_response_json(resp)

    def tree_search(self, response_json, value1, value2):
        count = 0
        for each in response_json[value1]:
            count += 1
            print(each[value2])

        return count

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

    def set_directory_structure(self, file):
        "Setup the required directory structure if it is not already present"
        try:
            self.screenshots_parent_dir = os.path.abspath(
                os.path.join(os.path.dirname(file), '..', 'result/screenshots'))
            if not os.path.exists(self.screenshots_parent_dir):
                os.makedirs(self.screenshots_parent_dir)
            self.logs_parent_dir = os.path.abspath(os.path.join(os.path.dirname(file), '..', 'result/logs'))
            if not os.path.exists(self.logs_parent_dir):
                os.makedirs(self.logs_parent_dir)
        except Exception as e:
            pass
