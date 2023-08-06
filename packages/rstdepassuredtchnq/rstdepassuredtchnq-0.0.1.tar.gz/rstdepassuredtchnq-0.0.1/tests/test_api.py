import inspect
import os

from rstdepassuredtchnq.core.base.apihelpers.api_methods import APIMethods
from rstdepassuredtchnq.core.base.apihelpers.common_methods import CommonMethods
from rstdepassuredtchnq.core.base.endpoints.api_helper import APIHelp
from rstdepassuredtchnq.core.base.format.pretty_base import PrettyFormat
from rstdepassuredtchnq.core.base.log.custom_logger import get_logger


class TestAPI:
    api_req = APIMethods()
    common_data = CommonMethods()
    pretty_format = PrettyFormat()
    log = get_logger("TestAPI")
    Base_url = "https://reqres.in"
    api_help = APIHelp(Base_url)
    cur_path = os.path.abspath(os.path.dirname(__file__))
    log_dir = os.path.join(cur_path, r"../payload")

    def setup_class(cls):
        print('To load tests data.')

    def test_get_users_page(self):
        # get users list
        get_user_response = self.api_help.get_users_list()
        print(get_user_response)

        # get users count of list
        json_resp = self.common_data.fetch_json(get_user_response.text, 'ad')
        self.log.info('Fetched Json Value in Get Request {} '.format(json_resp))
        initial_count = self.api_help.get_users_list_count(get_user_response)
        print('initial_count value is %s' % initial_count)

        # get users single user list
        get_single_user_response = self.api_help.get_single_user_list(2)
        print(get_single_user_response)

        # add new users list
        req_payload = self.common_data.read_payload(self.log_dir, 'create.json')
        add_new_user_response = self.api_help.add_new_user(req_payload)
        print(add_new_user_response)

        # fetch new user id
        id_val = self.api_help.get_new_user_id(add_new_user_response.json(), 'id')
        print(id_val)

        # get users single user list
        get_single_user_response = self.api_help.get_single_user_list(id_val)
        print(get_single_user_response)

        # get users list
        get_users_response = self.api_help.get_users_list()
        print(get_users_response)

        # get users count of list
        new_count = self.api_help.get_users_list_count(get_users_response)
        print('new_count value is %s' % new_count)

    def test_get_reqre_api(self):
        url = '{}/api/users'.format(self.Base_url)
        params = {'page': 2}

        resp = self.api_req.get_request(url, params)
        print('Received Response is %s' % resp.text)
        self.api_req.check_status(resp, '200')

        json_resp = self.common_data.fetch_json(resp.text, 'ad')
        self.log.info('Fetched Json Value in Get Request {} '.format(json_resp))

        json_data_resp = self.common_data.fetch_json_subnode(resp.text)
        self.log.info('Fetching Subnode Json Value in Get Request {} '.format(json_resp))

        first_node = json_data_resp['total']
        print('total ------>  {}'.format(first_node))

        second_node = json_data_resp['data'][0]['email']
        print('first_email  ------> {}'.format(second_node))

        first_name = [d['first_name'] for d in json_data_resp['data']]
        print('first_name ------> {}'.format(first_name))

        assert resp is not None
        self.log.info('Test %s passed.' % inspect.stack()[0][3])

    def test_delete_reqre_api(self):
        url = '{}/api/users/2'.format(self.Base_url)
        resp = self.api_req.delete_request(url)
        self.api_req.check_status(resp, '204')
        assert resp is not None
        self.log.info('Test %s passed.' % inspect.stack()[0][3])

    def test_post_body_json_no_header(self):
        req_payload = self.common_data.read_payload(self.log_dir, 'create.json')
        url = '{}/api/users'.format(self.Base_url)

        resp = self.api_req.post_request_no_header(url, req_payload)
        self.api_req.check_status(resp, '201')

        get_name_value = self.common_data.fetch_json(resp.text, 'name')
        self.log.info('Fetched Json Value - name - in Post Request {} '.format(get_name_value))

        get_id_value = self.common_data.fetch_json(resp.text, 'id')
        self.log.info('Fetched Json Value - ID - in Post Request {} '.format(get_id_value))

        assert resp is not None
        self.log.info('Test %s passed.' % inspect.stack()[0][3])

    def test_put_json(self):
        url = '{}/api/users/2'.format(self.Base_url)
        req_payload = self.common_data.read_payload(self.log_dir, 'update_user.json')

        resp = self.api_req.put_request_no_header(url, req_payload)
        self.api_req.check_status(resp, '200')

        get_name_value = self.common_data.fetch_json(resp.text, 'name')
        self.log.info('Fetched Json Value - name - in Put Request {} '.format(get_name_value))
        assert get_name_value == 'morpheus', 'Validated Updated Name with payload file'

        get_updated_at_value = self.common_data.fetch_json(resp.text, 'updatedAt')
        self.log.info('Fetched Json Value - updatedAt - in Put Request {} '.format(get_updated_at_value))
