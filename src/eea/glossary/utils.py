# -*- coding: utf-8 -*-
''' utils module '''
from zope.globalrequest import getRequest


def get_request_information():
    ''' returns authenticated user and his IP '''
    try:
        request = getRequest()
        user = request['AUTHENTICATED_USER']
        ip = request['REMOTE_ADDR']
        return user, ip
    except KeyError:
        return 'test', '127.0.0.1'  # running tests
