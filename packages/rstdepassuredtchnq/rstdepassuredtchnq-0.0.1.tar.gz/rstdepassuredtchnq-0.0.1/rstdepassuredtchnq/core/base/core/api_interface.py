from base64 import b64encode

import oauth2
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

from rstdepassuredtchnq.core.base.endpoints.users_api import UsersAPI
from rstdepassuredtchnq.core.base.format.pretty_base import PrettyFormat


class APIInterface(UsersAPI):

    def __init__(self, url):
        "Constructor"
        # make base_url available to all API endpoints
        self.base_url = url
        self.pretty_format = PrettyFormat()

    def set_auth_details(self, username, password):
        "encode auth details"
        user = username
        password = password
        b64login = b64encode(bytes('%s:%s' % (user, password), "utf-8"))

        return b64login.decode('utf-8')

    def set_header_details(self, auth_details=None):
        "make header details"
        if auth_details != '' and auth_details is not None:
            headers = {'Authorization': "Basic %s" % (auth_details)}
        else:
            headers = {'content-type': 'application/json'}

        return headers

    def oauth2_authentication(self, url):
        consumer = oauth2.Consumer(key='CONSUMER_KEY', secret='CONSUMER_SECRET')
        acess_token = oauth2.Token(key='ACCESS_KEY', secret='ACCESS_SECRET')
        client = oauth2.Client(consumer, acess_token)
        resp, content = client.request(url)
        return resp, content

    def api_key_authentication(self, url, api_key):
        actual_url = '{}&appid={}'.format(url, api_key)
        return actual_url

    def auth_token_authentication(self, url):
        sesion = requests.session()
        resp = sesion.get(url)
        # Below code will convert into HTML formate
        soup = BeautifulSoup(resp.text, 'lxml')

        return resp, soup

    def session_post(self, url, data):
        sesion = self.get_request_session()
        resp = sesion.post(url, data)

        return resp

    def basic_auth_token_authentication(self, url, header):
        # sesion = requests.session()
        # resp = sesion.get(url, headers=header)
        # return resp.json()

        sesion = self.get_request_session()
        sesion.headers.update({"Authorization": "Basic {}".format(header)})
        resp = sesion.get(url)
        return resp.json()

    def basic_auth_http_token_authentication(self, url, user_name, token):
        sesion = self.get_request_session()
        resp = sesion.get(url, auth=HTTPBasicAuth(username=user_name, password=token))
        return resp.json()

    def basic_auth_token_authentication_headers(self, url, headers, token):
        sesion = self.get_request_session()
        sesion.headers['X-TokenAuth'] = token
        resp = sesion.get(url)
        return resp.json()
