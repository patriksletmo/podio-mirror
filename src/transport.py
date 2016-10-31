import json

import requests

BASE_URL = "https://api.podio.com"

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'


def call_endpoint(endpoint, method=GET, parameters=None, headers=None):
    url = BASE_URL + endpoint
    headers = headers or {}

    if method == GET:
        response = requests.get(url, headers=headers)
    elif method == POST:
        response = requests.post(url, data=parameters, headers=headers)
    elif method == PUT:
        response = requests.put(url, data=parameters, headers=headers)
    elif method == DELETE:
        response = requests.delete(url, data=parameters, headers=headers)
    else:
        raise RuntimeError('Unknown method')

    response.raise_for_status()
    return response


def call_authenticated_endpoint(token, endpoint, method=GET, parameters=None, headers=None):
    headers = headers or {}
    headers['Authorization'] = 'OAuth2 ' + token

    if method != GET:
        headers['Content-Type'] = 'application/json'

    return call_endpoint(endpoint, method, json.dumps(parameters), headers)
