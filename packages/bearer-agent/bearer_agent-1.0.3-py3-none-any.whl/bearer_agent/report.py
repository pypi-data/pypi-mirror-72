# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from io import BytesIO
import re


from .agent import enqueue_report
from .util import current_time


CONNECT_STAGE = "ConnectStage"
REQUEST_STAGE = "RequestStage"
RESPONSE_STAGE = "ResponseStage"
BODIES_STAGE = "BodiesStage"


REQUEST_END = "REQUEST_END"
REQUEST_ERROR = "REQUEST_ERROR"

_STATE_ACTIVE = 0
_STATE_ENQUEUED = 1


LOG_TEMPLATE = {
    "port": 0,
    "protocol": None,
    "hostname": "",
    "path": "",
    "method": "",
    "url": "",
    "params": "",
    "requestHeaders": {},
    "responseHeaders": {},
    "statusCode": None,
    "requestBody": "",
    "responseBody": "",
    "errorCode": "",
    "errorFullMessage": "",
}


class ReportLog(object):
    def __init__(self):
        self.log = LOG_TEMPLATE.copy()
        self.request_body = BytesIO()
        self.response_body = BytesIO()
        self.start_at = current_time()
        self.ended_at = self.start_at
        self.disabled = False
        self.stage_type = CONNECT_STAGE
        self.state = _STATE_ACTIVE
        self.response_proxy = False

    @property
    def protocol(self):
        return self.log["protocol"]

    @protocol.setter
    def protocol(self, value):
        self.log["protocol"] = value

    def update(self, attrs, stage_type=None):
        self.log.update(attrs)
        if stage_type is not None:
            self.stage_type = stage_type

    def end_report(self, error_code="", error_msg=""):
        if self.state == _STATE_ENQUEUED:
            return

        report_type = REQUEST_END
        self.ended_at = current_time()

        self.log.update(
            {
                "stageType": self.stage_type,
                "startedAt": self.start_at,
                "endedAt": self.ended_at,
                "requestBody": self.request_body,
                "responseBody": self.response_body,
            }
        )

        if error_code:
            report_type = REQUEST_ERROR
            self.log.update({"errorCode": error_code, "errorFullMessage": error_msg})

        self.log["type"] = report_type

        self.state = _STATE_ENQUEUED
        enqueue_report(self)

    def process(self):
        request_headers = self.log["requestHeaders"]
        if isinstance(request_headers, tuple):
            fun, data = request_headers
            self.log["requestHeaders"] = fun(data)

        response_headers = self.log["responseHeaders"]
        if isinstance(response_headers, tuple):
            fun, data = response_headers
            self.log["responseHeaders"] = fun(data)

        self.log.update(
            {
                "instrumentation": {
                    "requestBenchmark": float(self.ended_at - self.start_at),
                    "responseContentLength": clen(self.log["responseHeaders"]),
                    "processingBeforeThreadBenchmark": -1.0,
                }
            }
        )
        return self.log


def clen(headers):
    for key, val in headers.items():
        if re.match("^content-length$", key, re.I):
            return int(val)
    return None
