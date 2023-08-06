
from base64 import b64encode

from rstdepassuredtchnq.core.base.apihelpers.api_methods import APIMethods
from rstdepassuredtchnq.core.base.apihelpers.common_methods import CommonMethods
from rstdepassuredtchnq.core.base.core.api_interface import APIInterface
from rstdepassuredtchnq.core.base.format.pretty_base import PrettyFormat
from rstdepassuredtchnq.core.base.log.custom_logger import get_logger


class TestAPIAuth:
    api_req = APIMethods()
    common_data = CommonMethods()
    pretty_format = PrettyFormat()
    log = get_logger("TestAPI")
    Base_url = ""
    api_obj = APIInterface(url=Base_url)

    def setup_class(cls):
        print('To load tests data.')

    # ********************* API Authentication Requests Test Cases *********************
    def test_oauth2_validation(self):
        timeline_endpoint = "https://api.twitter.com/1.1/statuses/home_timeline.json"
        resp, content = self.api_obj.oauth2_authentication(timeline_endpoint)
        tweets = self.common_data.load_json(content)

        for tweet in tweets:
            print('tweet values {}'.format(tweet['text']))

    def test_api_key_validation(self):
        url = "http://api.openweathermap.org/data/2.5/weather?q=London"
        base_url = self.api_obj.api_key_authentication(url, 'WEATHER_API_KEY')
        self.log.info('Fetched Json Value - updatedAt - in Put Request {} '.format(base_url))

        resp = self.api_req.get_request(base_url)
        # self.api_req.check_status(resp, '200')

    def test_form_auth_validation(self):
        url = "https://www.hackthis.co.uk/?login"
        req_payload = {"username": "test1", "password": "test1"}
        resp = self.api_req.post_request_no_header(url, req_payload)
        self.api_req.check_status(resp, '201')

    def test_auth_token_validation(self):
        url = "https://opensource-demo.orangehrmlive.com/"
        resp, soup = self.api_obj.auth_token_authentication(url)

        # Identifing element - Using CSS Selector in DOM
        csrk_token = soup.select("#divLoginForm #_csrf_token")[0].get('value')
        self.log.info("soup.select {}".format(soup.select("#csr_token")[0].get('value')))

        # # Identifing element -  Using Regex in DOM
        # pat = re.compile(r'<input type="hidden" name="_csrf_token" value="(.+?)" id="csrf_token">')
        # csrk_token = re.search(pat, resp.text)
        # self.log.info("Value is {} ".format(csrk_token.group(1)))

        login_data = {
            "actionID": "",
            "hdnUserTimeZoneOffset": "8",
            "_csrf_token": csrk_token,
            "txtUsername": "Admin",
            "txtPassword": "admin123",
            "Submit": "LOGIN"
        }

        req_url = "https://opensource-demo.orangehrmlive.com/index.php/auth/validateCredentials"

        respon = self.api_obj.session_post(req_url, login_data)
        self.log.info("respon is --> {}".format(respon.text))

    def test_basic_auth(self):
        auth_token = b"1176w182gyyg2737373h3hhhbe72hhj82j"
        user_name = b"deepika"
        base_url = "http://localhost:8080"
        actual_url = base_url + "/api/json?pretty=true"

        s = user_name + b":" + auth_token
        s = b64encode(s).decode('ascii')
        header = {"Authorization": "Basic " + s}

        self.api_obj.basic_auth_token_authentication(actual_url, s)

    def test_basic_auth_request_module(self):
        auth_token = "1176w182gyyg2737373h3hhhbe72hhj82j"
        user_name = "deepika"
        base_url = "http://localhost:8080"
        actual_url = base_url + "/api/json?pretty=true"

        self.api_obj.basic_auth_http_token_authentication(actual_url, user_name, auth_token)
