import json

from rstdepassuredtchnq.core.base.log.custom_logger import get_logger


class PrettyFormat:
    log = get_logger("PrettyFormat")

    def pretty_print_request(self, request):
        self.log.info('-----------Request-----------> Method = {} '.format(request.method))
        print('{}\n'.format(
            '-----------Request-----------> Method = {}'.format(request.method) + ' request url = {} '.format(
                request.url),
            '\n'.join('request headers = {}: {}'.format(k, v) for k, v in request.headers.items()),
            request.body)
        )

    def pretty_print_response(self, response):
        print('\n{}\n{}\n\n{}\n\n{}\n'.format(
            '<-----------Response-----------',
            'Status code:' + str(response.status_code),
            '\n'.join('response headers = {}: {}'.format(k, v) for k, v in response.headers.items()),
            response.text)
        )

    def pretty_print_response_json(self, response):
        """ pretty print response in json format.
            If failing to parse body in json format, print in text.
        """
        try:
            resp_data = response.json()
            resp_body = json.dumps(resp_data, indent=4)
        # if .json() fails, ValueError is raised.
        except ValueError:
            resp_body = response.text
        print('{}\n{}\n\n{}\n\n{}\n'.format(
            '<-----------Response-----------',
            'Status code:' + str(response.status_code),
            '\n'.join('{}: {}'.format(k, v) for k, v in response.headers.items()),
            resp_body
        ))
