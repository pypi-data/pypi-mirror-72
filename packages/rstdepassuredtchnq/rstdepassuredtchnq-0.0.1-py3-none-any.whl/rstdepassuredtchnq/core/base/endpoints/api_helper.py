from rstdepassuredtchnq.core.base.apihelpers.common_methods import CommonMethods
from rstdepassuredtchnq.core.base.core.api_interface import APIInterface


class APIHelp:

    def __init__(self, url, log_file_path=None):
        "Constructor"
        super(APIHelp, self).__init__()
        self.api_obj = APIInterface(url=url)
        self.common_data = CommonMethods()

    def get_users_list(self, auth_details=None):
        url_params = "page=2"
        headers = self.api_obj.set_header_details(auth_details)
        response = self.api_obj.get_users_list_page_header(url_param=url_params, headers=headers)
        print("json_response %s" % response.json())
        result_flag = True if response.status_code == 200 else False
        return response

    def get_users_list_count(self, response):
        total_count = self.common_data.tree_search(response.json(), 'data', 'id')
        print('total_count %s' % total_count)
        return total_count

    def get_single_user_list(self, user_id):
        url_params = user_id
        print('Passing url -> %s' % url_params)
        response = self.api_obj.get_single_users_list(url_param=url_params)
        print("json_response %s" % response)
        result_flag = True if response.status_code == 200 else False
        return response

    def add_new_user(self, data, headers=None):
        response = self.api_obj.add_user_to_list(data, headers)
        print("json_response %s" % response)
        result_flag = True if response.status_code == 201 else False
        return response

    def get_new_user_id(self, response, value):
        new_id = self.common_data.parse_from_response(response, value)
        print("new_id %s" % new_id)
        return new_id

