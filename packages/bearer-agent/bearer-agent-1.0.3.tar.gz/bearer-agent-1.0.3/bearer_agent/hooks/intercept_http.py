# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

import functools
from urllib.parse import urlparse, parse_qs
from http import client as _client
from socket import error as SocketError
import sys

import wrapt

from .. import agent
from ..report import ReportLog
from ..report import CONNECT_STAGE, REQUEST_STAGE, RESPONSE_STAGE
from ..util import reraise, ReadProxy, BufferProxy


def _pass_through(instance):
    if agent.is_disabled():
        return True

    return getattr(instance, "_bearer_disabled", False)


def httpclient_connect_wrapper(wrapped, instance, args, kwargs, protocol):
    if _pass_through(instance):
        return wrapped(*args, **kwargs)

    report = getattr(instance, "_bearer_report", ReportLog())

    if instance._tunnel_host:
        host = instance._tunnel_host
        port = instance._tunnel_port
    else:
        host = instance.host
        port = instance.port

    if not report.protocol:
        report.protocol = protocol

    report.update({"hostname": host, "port": port}, stage_type=CONNECT_STAGE)

    instance._bearer_report = report
    return wrapped(*args, **kwargs)


def process_request_headers(headers):
    headers_dict = {}
    for line in headers:
        key, val = line.decode("ascii").split(":", 1)
        headers_dict[key] = val.strip()
    return headers_dict


def httpclient_putrequest_wrapper(wrapped, instance, args, kwargs):
    if _pass_through(instance):
        return wrapped(*args, **kwargs)

    old_report = getattr(instance, "_bearer_report", None)
    report = ReportLog()
    if old_report is not None:
        report.update(
            {
                "hostname": old_report.log["hostname"],
                "port": old_report.log["port"],
                "protocol": old_report.log["protocol"],
            }
        )

    def parse_putrequest(method, url, **_kwargs):
        o = urlparse(url)
        path = o.path
        params = parse_qs(o.query)
        return {"method": method, "path": path, "params": params}

    report.update(parse_putrequest(*args, **kwargs))
    instance._bearer_report = report

    return wrapped(*args, **kwargs)


# TODO: support body given as file object
def httpclient_endheaders_wrapper(wrapped, instance, args, kwargs):
    if _pass_through(instance):
        return wrapped(*args, **kwargs)

    report = getattr(instance, "_bearer_report", None)
    if report is None:
        report = ReportLog()

    def parse_end_headers(conn, message_body=None, **_kwargs):
        # don't process headers there, only return relevant part as a list
        # this will be processed later
        return message_body, (process_request_headers, conn._buffer[1:])

    req_body, headers = parse_end_headers(instance, *args, **kwargs)

    report.update({"requestHeaders": headers}, stage_type=REQUEST_STAGE)

    if req_body is not None:
        if isinstance(req_body, str):
            report.request_body.write(req_body.encode("utf-8"))
        elif isinstance(req_body, bytes):
            report.request_body.write(req_body)
        else:
            # try to wrap the request body so we can still read it
            largs = list(args)
            if hasattr(req_body, "read"):
                proxy = ReadProxy(req_body, report.request_body)
            else:
                try:
                    # we check if it has a buffer interface,
                    # if not we will use an iterator over the body
                    memoryview(req_body)
                except TypeError:
                    try:
                        proxy = BufferProxy(iter(req_body), report.request_body)
                    except TypeError:
                        proxy = BufferProxy(req_body, report.request_body)
                else:
                    proxy = BufferProxy(req_body, report.request_body)

            largs[0] = proxy
            args = tuple(largs)

    instance._bearer_report = report

    return wrapped(*args, **kwargs)


def process_response_headers(headers):
    if isinstance(headers, list):
        headers_dict = {}
        for key, val in headers:
            headers_dict[key] = val
        return headers_dict
    return headers


def httpclient_getresponse_wrapper(wrapped, instance, args, kwargs):
    if _pass_through(instance):
        response = wrapped(*args, **kwargs)
        return response

    report = getattr(instance, "_bearer_report", None)
    disabled = getattr(instance, "_bearer_disabled", False)

    try:
        response = wrapped(*args, **kwargs)
        # update response stage
        report.update(
            {
                "statusCode": response.status,
                "responseHeaders": (process_response_headers, response.getheaders()),
            },
            stage_type=RESPONSE_STAGE,
        )
        response._bearer_report = report

        # ensure we pass the disabled attribute
        response._bearer_disabled = disabled
        return response
    except _client.ResponseNotReady:
        # do nothing is response is not ready, this is an app error
        reraise(*sys.exc_info())
    except (_client.HTTPException, SocketError) as exc:
        if report is not None:
            report.end_report("%r" % exc, exc)
        reraise(*sys.exc_info())
    finally:
        instance._bearer_report = report


def httpclient_connection_close_wrapper(wrapped, instance, args, kwargs):
    if _pass_through(instance):
        return wrapped(*args, **kwargs)

    report = getattr(instance, "_bearer_report", None)
    if report:
        report.end_report()

    return wrapped(*args, **kwargs)


def httpclient_response_close_wrapper(wrapped, instance, args, kwargs):
    if _pass_through(instance):
        return wrapped(*args, **kwargs)

    # send the report
    report = getattr(instance, "_bearer_report", None)
    if report is not None:
        report.end_report()

    instance._bearer_report = report

    return wrapped(*args, **kwargs)


def httpclient_response_read_wrapper(wrapped, instance, args, kwargs):
    if _pass_through(instance):
        return wrapped(*args, **kwargs)

    report = getattr(instance, "_bearer_report", None)
    if not report:
        return wrapped(*args, **kwargs)

    try:
        if report.response_proxy:
            return wrapped(*args, **kwargs)

        chunk = wrapped(*args, **kwargs)
        report.response_body.write(chunk)
        return chunk
    except (_client.HTTPException, SocketError) as exc:
        report.end_report("%r" % exc, exc)
        reraise(*sys.exc_info())
    finally:
        instance._bearer_report = report


def intercept(module):
    wrapt.wrap_function_wrapper(
        module,
        "HTTPConnection.connect",
        functools.partial(httpclient_connect_wrapper, protocol="http"),
    )

    wrapt.wrap_function_wrapper(
        module,
        "HTTPSConnection.connect",
        functools.partial(httpclient_connect_wrapper, protocol="https"),
    )

    wrapt.wrap_function_wrapper(
        module, "HTTPConnection.putrequest", httpclient_putrequest_wrapper
    )

    wrapt.wrap_function_wrapper(
        module, "HTTPConnection.endheaders", httpclient_endheaders_wrapper
    )

    wrapt.wrap_function_wrapper(
        module, "HTTPConnection.getresponse", httpclient_getresponse_wrapper
    )

    wrapt.wrap_function_wrapper(
        module, "HTTPConnection.close", httpclient_connection_close_wrapper
    )

    wrapt.wrap_function_wrapper(
        module, "HTTPResponse.close", httpclient_response_close_wrapper
    )

    wrapt.wrap_function_wrapper(
        module, "HTTPResponse.read", httpclient_response_read_wrapper
    )
