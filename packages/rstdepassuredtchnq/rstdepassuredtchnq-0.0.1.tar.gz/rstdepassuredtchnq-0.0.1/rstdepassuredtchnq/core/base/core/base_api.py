import requests
from urllib.error import HTTPError
from urllib.error import URLError

from bs4 import BeautifulSoup


class BaseAPI:
    def __init__(self, url=None):
        pass

    def get_req(self, url, headers={}):
        "Get request"
        json_response = None
        error = {}
        try:
            response = requests.get(url=url, headers=headers)
            print(response)
            try:
                json_response = response.json()
            except:
                json_response = None
        except (HTTPError, URLError) as e:
            error = e
            if isinstance(e, HTTPError):
                error_message = e.read()
                print("\n******\nGET Error: %s %s" %
                      (url, error_message))
            elif (e.reason.args[0] == 10061):
                print(
                    "\033[1;31m\nURL open error: Please check if the API server is up or there is any other issue accessing the URL\033[1;m")
                raise e
            else:
                print(e.reason.args)
                # bubble error back up after printing relevant details
                raise e  # We raise error only when unknown errors occurs (other than HTTP error and url open error 10061)
        print('\nActual Get Response -> %s \n' % response.json())
        assert response is not None
        return response
        # return {'response_code': response.status_code, 'text': response.text, 'json_response': json_response,
        #         'error': error,
        #         'response': response}

    def post_req(self, url, params=None, data=None, json=None, headers={}):
        "Post request"
        error = {}
        json_response = None
        try:
            response = requests.post(url, params=params, json=json, headers=headers)
            try:
                json_response = response.json()
            except:
                json_response = None
        except (HTTPError, URLError) as e:
            error = e
            if isinstance(e, HTTPError, URLError):
                error_message = e.read()
                print("\n******\nPOST Error: %s %s %s" %
                      (url, error_message, str(json)))
            elif (e.reason.args[0] == 10061):
                print(
                    "\033[1;31m\nURL open error: Please check if the API server is up or there is any other issue accessing the URL\033[1;m")
            else:
                print(e.reason.args)
                # bubble error back up after printing relevant details
            raise e
        print('\nActual Post Response -> %s \n' % response.json())
        assert response is not None
        return response
        # return {'response_code': response.status_code, 'text': response.text, 'json_response': json_response,
        #         'error': error,
        #         'response': response}

    def delete_req(self, url, headers={}):
        "Delete request"
        response = False
        error = {}
        try:
            response = requests.delete(url, headers=headers)
            try:
                json_response = response.json()
            except:
                json_response = None

        except (HTTPError, URLError) as e:
            error = e
            if isinstance(e, HTTPError):
                error_message = e.read()
                print("\n******\nPUT Error: %s %s %s" %
                      (url, error_message, str(URLError)))
            elif (e.reason.args[0] == 10061):
                print(
                    "\033[1;31m\nURL open error: Please check if the API server is up or there is any other issue accessing the URL\033[1;m")
            else:
                print(str(e.reason.args))
            # bubble error back up after printing relevant details
            raise e
        print('\nActual Delete Response -> %s \n' % response.json())
        assert response is not None
        return {'response': response.status_code, 'text': response.text, 'json_response': json_response, 'error': error}

    def put_req(self, url, json=None, headers={}):
        "Put request"
        error = {}
        response = False
        try:
            response = requests.put(url, json=json, headers=headers)
            try:
                json_response = response.json()
            except:
                json_response = None


        except (HTTPError, URLError) as e:
            error = e
            if isinstance(e, HTTPError):
                error_message = e.read()
                print("\n******\nPUT Error: %s %s %s" %
                      (url, error_message, str(HTTPError)))
            elif (e.reason.args[0] == 10061):
                print(
                    "\033[1;31m\nURL open error: Please check if the API server is up or there is any other issue accessing the URL\033[1;m")
            else:
                print(str(e.reason.args))
            # bubble error back up after printing relevant details
            raise e

        print('\nActual Put Response -> %s \n' % response.json())
        assert response is not None
        return {'response': response.status_code, 'text': response.text, 'json_response': json_response, 'error': error}

    def get_request_session(self):
        sesion = requests.session()
        assert sesion is not None
        return sesion
