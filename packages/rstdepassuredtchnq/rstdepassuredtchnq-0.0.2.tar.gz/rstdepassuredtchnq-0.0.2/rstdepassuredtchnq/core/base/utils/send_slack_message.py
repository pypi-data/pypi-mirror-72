import json, os, requests

from rstdepassuredtchnq.core.base.apihelpers.common_methods import CommonMethods

cur_path = os.path.abspath(os.path.dirname(__file__))
log_dir = os.path.join(cur_path, r"../../../../payload")


class SlackMessage:
    def post_file_info_to_slack(self):
        url = "https://hooks.slack.com/services/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"  # Add your Slack incoming webhook url here

        test_report_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'report/logs',
                                                        'execution.log'))  # Change report file name & address here

        with open(test_report_file, "r") as in_file:
            testdata = ""
            for line in in_file:
                testdata = testdata + '\n' + line

        # Set Slack Pass Fail bar indicator color according to test results
        if 'FAILED' or 'Error' in testdata:
            bar_color = "#ff0000"
        else:
            bar_color = "#36a64f"

        data = {"attachments": [
            {"color": bar_color,
             "title": "Test Report",
             "text": testdata}
        ]}

        json_params_encoded = json.dumps(data)
        slack_response = requests.post(url=url, data=json_params_encoded, headers={"Content-type": "application/json"})
        if slack_response.text == 'ok':
            print('\n Successfully posted pytest report on Slack channel')
        else:
            print('\n Something went wrong. Unable to post pytest report on Slack channel. Slack Response:',
                  slack_response)

    def post_file_to_slack(self, data):
        url = "https://hooks.slack.com/services/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"  # Add your Slack incoming webhook url here

        json_params_encoded = json.dumps(data)
        slack_response = requests.post(url=url, data=json_params_encoded, headers={"Content-type": "application/json"})
        if slack_response.text == 'ok':
            print('\n Successfully posted report on Slack channel')
        else:
            print('\n Something went wrong. Unable to post pytest report on Slack channel. Slack Response:',
                  slack_response)


if __name__ == '__main__':
    slack = SlackMessage()
    common_data = CommonMethods()
    req_payload = common_data.read_payload(log_dir, 'slack_message.json')
    slack.post_file_info_to_slack()
    slack.post_file_to_slack(req_payload)
