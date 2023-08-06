from rstdepassuredtchnq.core.base.core.base_api import BaseAPI


class UsersAPI(BaseAPI):
    def users_url(self, suffix=''):
        return self.base_url + '/api/users' + suffix

    def get_users_list_page_header(self, url_param, headers):
        url = self.users_url('?%s') % url_param
        print('Passing Url -> %s' % url)
        response = self.get_req(url, headers=headers)
        return response

    def get_users_list_page(self, url_param):
        url = self.users_url('?%s') % url_param
        print('Passing Url -> %s' % url)
        response = self.get_req(url)
        return response

    def get_single_users_list(self, url_param):
        url = self.users_url('/%s') % url_param
        print('Passing Url -> %s' % url)
        response = self.get_req(url)
        return response

    def add_user_to_list(self, data, headers):
        url = self.users_url()
        print('Passing Url -> %s' % url)
        response = self.post_req(url=url, json=data, headers=headers)
        return response
