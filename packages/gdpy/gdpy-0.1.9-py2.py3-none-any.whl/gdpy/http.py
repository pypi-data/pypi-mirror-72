# -*- coding: utf-8 -*-
"""
gdpy.http
对requests中的Session Request做了简单的封装
"""
from __future__ import absolute_import

import requests
from requests.structures import CaseInsensitiveDict

from .compat import to_json
from .defaults import connection_pool_size
from .exceptions import RequestError


class Session(object):
    def __init__(self):
        self.session = requests.Session()

        psize = connection_pool_size
        self.session.mount('http://', requests.adapters.HTTPAdapter(pool_connections=psize, pool_maxsize=psize))
        self.session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=psize, pool_maxsize=psize))

    def do_request(self, req, timeout):
        try:
            return Response(self.session.request(req.method, req.url,
                                                 auth=req.auth,
                                                 data=req.data,
                                                 params=req.params,
                                                 files=req.files,
                                                 headers=req.headers,
                                                 stream=True,
                                                 timeout=timeout))
        except requests.RequestException as e:
            raise RequestError(e)


class Request(object):
    def __init__(self, method, auth, url,
                 data=None,
                 params=None,
                 headers=None,
                 content_type=None,
                 files=None,
                 app_name=''):
        self.method = method
        self.url = url
        self.data = _convert_request_body(data, content_type)
        self.params = params or {}
        self.auth = auth
        self.files = files

        if not isinstance(headers, CaseInsensitiveDict):
            self.headers = CaseInsensitiveDict(headers)
        else:
            self.headers = headers

        if data and not content_type:
            self.headers['content-type'] = 'application/json'


_CHUNK_SIZE = 8 * 1024


class Response(object):
    def __init__(self, response):
        self.response = response
        self.status = response.status_code
        self.headers = response.headers

    def read(self, amt=None):
        if amt is None:
            content = b''
            for chunk in self.response.iter_content(_CHUNK_SIZE):
                content += chunk
            return content
        else:
            try:
                return next(self.response.iter_content(amt))
            except StopIteration:
                return b''

    def __iter__(self):
        return self.response.iter_content(_CHUNK_SIZE)


def _convert_request_body(data, content_type=None):
    if not content_type or content_type in ['application/json']:
        return to_json(data)
    return data
