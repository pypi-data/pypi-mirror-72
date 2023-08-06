import unittest
from unittest.mock import patch, Mock

from rstdepassuredtchnq.core.base.apihelpers.request_methods import BaseAPIHelper


class BasicTests(unittest.TestCase):
    user_val = BaseAPIHelper()
    base_url = "https://reqres.in/api/users"

    @patch('rstdepassuredtchnq.core.base.apihelpers.request_methods.requests.get')  # Mock 'requests' module 'get' method.
    def test_request_response_with_decorator(self, mock_get):
        users_data = [{
            "id": 0,
            "first_name": "Dell",
            "last_name": "Norval",
            "phone": "994-979-3976"
        }]

        """Mocking using a decorator"""
        mock_get.return_value.status_code = 401  # Mock status code of response.
        mock_get.return_value.json.return_value = users_data  # Mock response.

        response = self.user_val.get_request(self.base_url)
        print("Value is %s " % response.status_code)
        print("Value is %s " % response.json())

        # Assert that the request-response cycle completed successfully.
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), users_data)

    def test_request_response_with_context_manager(self):
        """Mocking using a context manager"""
        with patch('rstdepassuredtchnq.core.base.apihelpers.request_methods.requests.get') as mock_get:
            # Configure the mock to return a response with status code 200.
            mock_get.return_value.status_code = 500

            # Call the function, which will send a request to the server.
            response = self.user_val.get_request(self.base_url)

        # Assert that the request-response cycle completed successfully.
        self.assertEqual(response.status_code, 500)

    def test_request_response_with_patcher(self):
        """Mocking using a patcher"""
        mock_get_patcher = patch('rstdepassuredtchnq.core.base.apihelpers.request_methods.requests.get')
        users = [{
            "id": 0,
            "first_name": "Dell",
            "last_name": "Norval",
            "phone": "994-979-3976"
        }]

        # Start patching 'requests.get'.
        mock_get = mock_get_patcher.start()

        # Configure the mock to return a response with status code 200.
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = users

        # Call the service, which will send a request to the server.
        response = self.user_val.get_request(self.base_url)

        # Stop patching 'requests'.
        mock_get_patcher.stop()

        # Assert that the request-response cycle completed successfully.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), users)

    def test_mock_whole_function_with_patcher(self):
        """Mocking a whole function"""
        mock_get_patcher = patch('rstdepassuredtchnq.core.base.apihelpers.request_methods.requests.get')
        users = [{
            "id": 0,
            "first_name": "Dell",
            "last_name": "Norval",
            "phone": "994-979-3976"
        }]

        # Start patching 'requests.get'.
        mock_get = mock_get_patcher.start()

        # Configure the mock to return a response with status code 200 and a list of users.
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = users

        # Call the service, which will send a request to the server.
        response = self.user_val.get_request(self.base_url)

        # Stop patching 'requests'.
        mock_get_patcher.stop()

        # Assert that the request-response cycle completed successfully.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), users)

    @patch('rstdepassuredtchnq.core.base.apihelpers.request_methods.BaseAPIHelper.get_request')
    def test_get_one_user(self, mock_get_users):
        """
        Test for getting one user using their userID
        Demonstrates mocking third party functions
        """
        users = [
            {'phone': '514-794-6957', 'first_name': 'Brant',
             'last_name': 'Mekhi', 'id': 0},
            {'phone': '772-370-0117', 'first_name': 'Thalia',
             'last_name': 'Kenyatta', 'id': 1},
            {'phone': '176-290-7637', 'first_name': 'Destin',
             'last_name': 'Soledad', 'id': 2}
        ]
        mock_get_users.return_value = Mock()
        mock_get_users.return_value.json.return_value = users
        user = self.user_val.get_request(self.base_url)
        self.assertEqual(user.json(), users)


if __name__ == "__main__":
    unittest.main()
