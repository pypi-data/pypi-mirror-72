import os
import time

from werkzeug.local import LocalProxy


class Gobits:
    """
    A small class that gathers information (bits) for a pub/sub message payload.

    Attributes:
        _request            Holds information about the cloud function request.
        _context            Holds information about the cloud function context.
        created             Date of creation in milliseconds since epoch (UTC).
        project             The source GCP project.
        function_name       Name of the processing cloud function.
        function_version    Version of the processing cloud function.
    """

    def __init__(self, request: LocalProxy = None, context=None):
        self._request = request
        self._context = context
        self.created = str(int(round(time.time() * 1000)))
        self.project = os.getenv('X_GOOGLE_GCP_PROJECT')
        self.function_name = os.getenv('X_GOOGLE_FUNCTION_NAME')
        self.function_version = os.getenv('X_GOOGLE_FUNCTION_VERSION')

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, value):
        self._request = value

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value

    @property
    def id(self):
        if self._request:
            return self._request.get('environ', {}).get('HTTP_FUNCTION_EXECUTION_ID')
        elif self._context:
            return self._context.get('event_id')

    def to_json(self):
        all = dict(vars(self), id=self.id)
        public = {k: v for (k, v) in all.items() if not k.startswith('_')}
        return public
