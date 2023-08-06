import os

from rstdepassuredtchnq.core.base.apihelpers.api_methods import APIMethods
from rstdepassuredtchnq.core.base.apihelpers.api_methods import APIMethods
from rstdepassuredtchnq.core.base.apihelpers.common_methods import CommonMethods
from rstdepassuredtchnq.core.base.endpoints.api_helper import APIHelp
from rstdepassuredtchnq.core.base.format.pretty_base import PrettyFormat
from rstdepassuredtchnq.core.base.log.custom_logger import get_logger


class TestBase:
    cur_path = os.path.abspath(os.path.dirname(__file__))
    paylod_log_dir = os.path.join(cur_path, r"../payload")
    api_req = APIMethods()
    common_data = CommonMethods()
    pretty_format = PrettyFormat()
    Base_url = "https://reqres.in"
    api_help = APIHelp(Base_url)
    log = get_logger("TestBase")

    @classmethod
    def setup_class(cls):
        print('To load tests data.')
        cls.log.info('To load tests data.')
        cls.common_data.set_directory_structure(cls.cur_path + "../")

    @classmethod
    def teardown_class(cls):
        print('Ended --------- To load tests data.')
        cls.log.info('Ended --------- To load tests data.')
