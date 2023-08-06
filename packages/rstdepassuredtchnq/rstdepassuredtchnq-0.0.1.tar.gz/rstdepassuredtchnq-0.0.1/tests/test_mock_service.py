import inspect

from rstdepassuredtchnq.core.base.apihelpers.api_methods import APIMethods
from rstdepassuredtchnq.core.base.format.pretty_base import PrettyFormat
from rstdepassuredtchnq.core.base.log.custom_logger import get_logger


class TestMockServiceAPI:
    api_req = APIMethods()
    pretty_format = PrettyFormat()
    log = get_logger("TestAPI")

    def setup_class(cls):
        print('To load tests data.')

    def test_mock_service(self):
        print('Calling %s.' % inspect.stack()[0][3])
        base_url = f'http://127.0.0.1:5000/json'
        resp = self.api_req.get_request(url=base_url)
        self.api_req.check_status(resp, '200')
        assert resp is not None
        print('Test %s passed. {}'.format(resp.status_code))
        value = resp.json()
        assert value["code"] == 1
        print('Test %s passed.' % inspect.stack()[0][3])
        self.log.info('Test %s passed.' % inspect.stack()[0][3])
