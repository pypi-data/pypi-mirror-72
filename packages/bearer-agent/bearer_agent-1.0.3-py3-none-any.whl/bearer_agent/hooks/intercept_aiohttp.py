# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.


import sys
from urllib.parse import parse_qs, urlencode

import wrapt

from ..report import ReportLog
from ..report import CONNECT_STAGE, REQUEST_STAGE, RESPONSE_STAGE
from ..util import reraise, ReadProxy, BufferProxy, AsyncReadProxy


def clientrequest_update_host_wrapper(wrapped, instance, args, kwargs):
    report = getattr(instance, "_bearer_report", None)
    if report is None:
        report = ReportLog()
        if instance.is_ssl():
            report.protocol = "https"
        else:
            report.protocol = "http"

        url = instance.original_url

        report.update(
            {
                "hostname": instance.host,
                "port": instance.port,
                "method": instance.method,
                "path": url.raw_path,
                "params": parse_qs(url.query_string),
            },
            stage_type=CONNECT_STAGE,
        )
        instance._bearer_report = report

    try:
        return wrapped(*args, **kwargs)
    except Exception as exc:
        report.stage_type = CONNECT_STAGE
        report.end_report("%r" % exc, exc)
        reraise(*sys.exc_info())


def clientrequest_update_body_from_data_wrapper(wrapped, instance, args, kwargs):
    report = getattr(instance, "_bearer_report")

    req_body = list(args)[0]

    if req_body is not None:
        if isinstance(req_body, str):
            report.request_body.write(req_body.encode("utf-8"))
        elif isinstance(req_body, bytes):
            report.request_body.write(req_body)
        else:
            if hasattr(req_body, "read"):
                proxy = ReadProxy(req_body, report.request_body)
            elif hasattr(req_body, "_gen_form_urlencode"):
                # formdata type
                data = []
                for type_options, _, value in req_body._fields:
                    data.append((type_options["name"], value))

                charset = (
                    req_body._charset if req_body._charset is not None else "utf-8"
                )

                report.request_body.write(
                    urlencode(data, doseq=True, encoding=charset).encode()
                )
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
            instance.body = proxy

    return wrapped(*args, **kwargs)


# TODO: patch headers support in bearer to support multiple headers with identical keys (like cookies)
def process_request_headers(headers):
    headers_dict = {}
    for hdr_name, hdr_val in headers.items():
        headers_dict[hdr_name] = hdr_val
    return headers_dict


def clientrequest_send_wrapper(wrapped, instance, args, kwargs):
    report = getattr(instance, "_bearer_report")

    headers = (process_request_headers, instance.headers)
    report.update({"requestHeaders": headers}, stage_type=REQUEST_STAGE)

    largs = list(args)
    conn = largs[0]
    conn._bearer_report = report
    largs[0] = conn
    args = tuple(largs)

    async def _send():
        response = await wrapped(*args, **kwargs)
        response._bearer_report = report
        return response

    try:
        return _send()
    except Exception as exc:
        report.stage_type = REQUEST_STAGE
        report.end_report("%r" % exc, exc)
        reraise(*sys.exc_info())
    finally:
        instance._bearer_report = report


def process_response_headers(headers):
    headers_dict = {}
    for key, val in headers:
        headers_dict[key.decode("ascii")] = val.decode("ascii")
    return headers_dict


def client_reqrep_response_start_wrapper(wrapped, instance, args, kwargs):
    report = getattr(instance, "_bearer_report", None)

    if report is None:
        return wrapped(*args, **kwargs)

    async def _start():
        ret = await wrapped(*args, **kwargs)
        # update response stage
        report.update(
            {
                "statusCode": instance.status,
                "responseHeaders": (process_response_headers, instance._raw_headers),
            },
            stage_type=RESPONSE_STAGE,
        )
        instance.content = AsyncReadProxy(instance.content, report.response_body)
        instance._bearer_report = report
        return ret

    try:
        return _start()
    except Exception as exc:
        report.stage_type = RESPONSE_STAGE
        report.end_report("%r" % exc, exc)
        reraise(*sys.exc_info())


def connector_connection_close_wrapper(wrapped, instance, args, kwargs):
    report = getattr(instance, "_bearer_report", None)
    if report is not None:
        report.end_report()

    return wrapped(*args, **kwargs)


def connector_connection_release_wrapper(wrapped, instance, args, kwargs):
    report = getattr(instance, "_bearer_report", None)
    if report is not None:
        report.end_report()
        delattr(instance, "_bearer_report")
    return wrapped(*args, **kwargs)


def intercept(module):
    wrapt.wrap_function_wrapper(
        module,
        "client_reqrep.ClientRequest.update_host",
        clientrequest_update_host_wrapper,
    )

    wrapt.wrap_function_wrapper(
        module,
        "client_reqrep.ClientRequest.update_body_from_data",
        clientrequest_update_body_from_data_wrapper,
    )

    wrapt.wrap_function_wrapper(
        module, "client_reqrep.ClientRequest.send", clientrequest_send_wrapper
    )

    wrapt.wrap_function_wrapper(
        module,
        "client_reqrep.ClientResponse.start",
        client_reqrep_response_start_wrapper,
    )

    wrapt.wrap_function_wrapper(
        module, "connector.Connection.close", connector_connection_close_wrapper
    )

    wrapt.wrap_function_wrapper(
        module, "connector.Connection.release", connector_connection_release_wrapper
    )
