# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.


import functools

import wrapt

from .intercept_http import (
    httpclient_connect_wrapper,
    httpclient_putrequest_wrapper,
    httpclient_endheaders_wrapper,
    httpclient_getresponse_wrapper,
    httpclient_connection_close_wrapper,
)

from ..util import BufferProxy


def urllib3_response_release_conn_wrapper(wrapped, instance, args, kwargs):
    response = getattr(instance, "_original_response")
    report = getattr(response, "_bearer_report", None)

    if report is not None:
        report.end_report()
        instance._original_response._bearer_report = report

    conn = getattr(instance, "_connection", None)
    if conn is not None:
        instance._connection._bearer_report = report

    return wrapped(*args, **kwargs)


def urllib3_response_stream_wrapper(wrapped, instance, args, kwargs):
    response = getattr(instance, "_original_response")
    report = getattr(response, "_bearer_report", None)

    if not report:
        return wrapped(*args, **kwargs)

    stream = wrapped(*args, **kwargs)
    proxy = BufferProxy(stream, report.response_body)

    report.response_proxy = True

    instance._original_response._bearer_report = report

    return proxy


def intercept(module):
    wrapt.wrap_function_wrapper(
        module,
        "connection.HTTPConnection.connect",
        functools.partial(httpclient_connect_wrapper, protocol="http"),
    )

    wrapt.wrap_function_wrapper(
        module,
        "connection.HTTPSConnection.connect",
        functools.partial(httpclient_connect_wrapper, protocol="https"),
    )

    wrapt.wrap_function_wrapper(
        module, "connection.HTTPConnection.putrequest", httpclient_putrequest_wrapper
    )

    wrapt.wrap_function_wrapper(
        module, "connection.HTTPConnection.endheaders", httpclient_endheaders_wrapper
    )

    wrapt.wrap_function_wrapper(
        module, "connection.HTTPConnection.getresponse", httpclient_getresponse_wrapper
    )

    wrapt.wrap_function_wrapper(
        module, "connection.HTTPConnection.close", httpclient_connection_close_wrapper
    )

    wrapt.wrap_function_wrapper(
        module,
        "response.HTTPResponse.release_conn",
        urllib3_response_release_conn_wrapper,
    )

    wrapt.wrap_function_wrapper(
        module, "response.HTTPResponse.stream", urllib3_response_stream_wrapper
    )
