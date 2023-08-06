#!/usr/bin/env python3

import requests


class BaseApi:
    version = None

    def __init__(self, domain, api_key):
        self.endpoint = "https://{}.scuttle.bluesoul.net/api/v{}".format(
            domain, type(self).version
        )
        self.api_key = api_key

    def request(self, namespace, value=None, data=None):
        method = 'get' if data is None else 'post'
        send = {'headers': {"Authorization": "Bearer {}".format(self.api_key)}}
        if data is not None:
            send['data'] = data
        response = getattr(requests, method)(
            "{}/{}".format(self.endpoint, namespace.format(value)), **send
        )
        return response.json()
