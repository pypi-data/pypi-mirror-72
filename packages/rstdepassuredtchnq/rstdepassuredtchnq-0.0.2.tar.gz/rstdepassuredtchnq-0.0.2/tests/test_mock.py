import unittest
from unittest.mock import patch

from rstdepassuredtchnq.core.base.apihelpers.common_methods import CommonMethods
from rstdepassuredtchnq.core.base.apihelpers.request_methods import BaseAPIHelper


class MockTests(unittest.TestCase):
    user_val = BaseAPIHelper()
    common_data = CommonMethods()
    base_url = "https://localhost/api/users"

    @patch('base.apihelpers.request_methods.requests.get')  # Mock 'requests' module 'get' method.
    def test_request_response_with_decorator(self, mock_get):
        users_data = {"page": 1, "per_page": 6, "total": 12, "total_pages": 2, "data": [
            {"id": 1, "name": "cerulean", "year": 2000, "color": "#98B2D1", "pantone_value": "15-4020"},
            {"id": 2, "name": "fuchsia rose", "year": 2001, "color": "#C74375", "pantone_value": "17-2031"},
            {"id": 3, "name": "true red", "year": 2002, "color": "#BF1932", "pantone_value": "19-1664"},
            {"id": 4, "name": "aqua sky", "year": 2003, "color": "#7BC4C4", "pantone_value": "14-4811"},
            {"id": 5, "name": "tigerlily", "year": 2004, "color": "#E2583E", "pantone_value": "17-1456"},
            {"id": 6, "name": "blue turquoise", "year": 2005, "color": "#53B0AE", "pantone_value": "15-5217"}],
                      "ad": {"company": "StatusCode Weekly", "url": "http://statuscode.org/",
                             "text": "A weekly newsletter focusing on software development, infrastructure, the server, performance, and the stack end of things."}}

        """Mocking using a decorator"""
        mock_get.return_value.url = str(self.base_url)
        mock_get.return_value.text = str(users_data)
        mock_get.return_value.status_code = 200  # Mock status code of response.
        mock_get.return_value.json.return_value = users_data
        mock_get.return_value.content = users_data  # Mock response.

        response = self.user_val.get_request(self.base_url)
        print('Received Response is %s' % response.text)
        print("Value is %s " % response.status_code)
        print("Value is %s " % response.json())
        print("Value of -> %s" % self.common_data.parse_from_response(response.json(), 'ad'))
        print("Value of -> %s" % self.common_data.parse_subnode_from_response(response.json(), 'ad', 'company'))
        self.common_data.parse_from_response(response.json(), 'ad')
        # Assert that the request-response cycle completed successfully.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), users_data)


if __name__ == "__main__":
    unittest.main()
