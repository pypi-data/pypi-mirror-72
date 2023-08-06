import os
import time

from werkzeug.local import LocalProxy


class Gobits:
    """
    A small class that gathers information (bits) for a pub/sub message payload.

    Attributes:
        _request                Holds information about the cloud function request.
        _context                Holds information about the cloud function context.
        processed               Time of processing in milliseconds since epoch (UTC).
        gcp_project             The source GCP project.
        execution_type          Type of the service processing the message.
        execution_trigger_type  Type of the trigger invoking the processor.
        function_name           Name of the processing cloud function.
        function_version        Version of the processing cloud function.
    """

    def __init__(self, request: LocalProxy = None, context=None):
        self._request = request
        self._context = context
        self.processed = str(int(round(time.time() * 1000)))
        self.gcp_project = os.getenv('X_GOOGLE_GCP_PROJECT')
        self.execution_type = 'cloud_function' if os.getenv('X_GOOGLE_FUNCTION_NAME') else None
        self.execution_trigger_type = os.getenv('FUNCTION_TRIGGER_TYPE')
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
    def execution_id(self):
        if self._request:
            return self._request.headers.get('Function-Execution-Id')

    @property
    def event_id(self):
        if self._context:
            return self._context.event_id

    def to_json(self):

        all = dict(
            vars(self),
            event_id=self.event_id,
            execution_id=self.execution_id
        )

        public = {k: v for (k, v) in all.items() if not k.startswith('_')}

        return public
