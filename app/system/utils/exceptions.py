__author__ = 'rey'

from tornado.web import HTTPError


class ChimeraHTTPError(HTTPError):

    def __init__(self, status_code, log_message=None, *args, **kwargs):
        HTTPError.__init__(self, status_code, log_message, *args, **kwargs)
        self.error_message = kwargs.get('error_message', None)
