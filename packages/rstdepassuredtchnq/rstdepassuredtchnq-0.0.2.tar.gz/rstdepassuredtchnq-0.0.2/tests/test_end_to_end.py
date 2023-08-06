import os

from rstdepassuredtchnq.core.base.apihelpers.api_methods import APIMethods
from rstdepassuredtchnq.core.base.apihelpers.common_methods import CommonMethods
from rstdepassuredtchnq.core.base.format.pretty_base import PrettyFormat
from rstdepassuredtchnq.core.base.log.custom_logger import get_logger


class TestEndtoEndAPI:
    api_req = APIMethods()
    common_data = CommonMethods()
    pretty_format = PrettyFormat()
    log = get_logger("TestAPI")
    cur_path = os.path.abspath(os.path.dirname(__file__))
    log_dir = os.path.join(cur_path, r"../payload")

    def setup_class(cls):
        print('To load tests data.')

    def test_end_to_end(self):
        # Request 1
        base_url = 'http://thetestingworldapi.com/api/studentsDetails'
        req_payload = self.common_data.read_payload(self.log_dir,'create_student_record.json')
        resp = self.api_req.post_request_no_header(base_url, req_payload)
        self.api_req.check_status(resp, '201')

        get_id_value = self.common_data.fetch_json(resp.text, 'id')
        self.log.info('Fetched Json Value - id - in Put Request %s ' % str(get_id_value))
        # assert get_id_value == 62, "Validated the ID value"

        # Request 2
        tech_base_url = 'http://thetestingworldapi.com/api/technicalskills'
        req_payload = self.common_data.read_payload(self.log_dir,'update_technical_skill.json')
        req_payload['id'] = get_id_value
        req_payload['st_id'] = get_id_value
        self.log.info('Updated req_payload in End to End {} '.format(req_payload))

        resp = self.api_req.post_request_no_header(tech_base_url, req_payload)
        print("tech_base_url = {}".format(resp.text))
        self.api_req.check_status(resp, '200')
        get_msg_value = self.common_data.fetch_json(resp.text, 'msg')
        self.log.info('Fetched Json Value - get_msg_value - in Put Request %s ' % get_msg_value)
        assert get_msg_value == "Add  data success"

        # Request 3
        add_base_url = 'http://thetestingworldapi.com/api/addresses'
        req_payload = self.common_data.read_payload(self.log_dir,'tech_update_stud_address.json')
        req_payload['st_id'] = get_id_value
        resp = self.api_req.post_request_no_header(add_base_url, req_payload)
        get_message_value = self.common_data.fetch_json(resp.text, 'Message')
        self.log.info('Fetched Json Value - get_message_value - in Put Request %s ' % get_message_value)
