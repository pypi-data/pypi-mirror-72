# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

import json
import re
import zlib
import urllib.parse

from urllib3.response import MultiDecoder, GzipDecoder, DeflateDecoder


FILTERED = "[FILTERED]"


class ContentType(object):

    PLAIN = 0
    JSON = 1
    FORM = 2
    BINARY = 3


def _get_decoder(mode):
    if "," in mode:
        return MultiDecoder(mode)

    if mode == "gzip":
        return GzipDecoder()

    return DeflateDecoder()


class Sanitizer(object):

    non_binary_re = re.compile("json|text|xml|x-www-form-urlencoded", re.I)
    json_re = re.compile("^application/json", re.I)
    form_re = re.compile("^application/x-www-form-urlencoded", re.I)

    MAX_BODY_SIZE = 1024 * 1024  # 1mb
    CONTENT_DECODERS = ["gzip", "deflate"]
    DECODER_ERROR_CLASSES = (IOError, zlib.error)

    def __init__(self, cfg):
        self.strip_sensitive_regex = cfg.strip_sensitive_regex
        self.strip_sensitive_keys = cfg.strip_sensitive_keys

    def _is_filtered_key(self, key):
        if self.strip_sensitive_keys and self.strip_sensitive_keys.match(key):
            return True

        return False

    def _sanitize_string(self, value):
        if self.strip_sensitive_regex:
            return self.strip_sensitive_regex.sub(FILTERED, value)
        return value

    def _sanitize_dict(self, d):
        ret = {}
        for key, value in d.items():
            if self._is_filtered_key(key):
                ret[key] = FILTERED
                continue

            ret[key] = self._sanitize_value(value)
        return ret

    def _sanitize_value(self, value):
        if isinstance(value, list):
            return [self._sanitize_value(item) for item in value]
        elif isinstance(value, dict):
            return self._sanitize_dict(value)
        elif isinstance(value, str):
            return self._sanitize_string(value)
        return value

    def _init_decoder(self, content_encoding):
        if content_encoding in self.CONTENT_DECODERS:
            return _get_decoder(content_encoding)
        elif "," in content_encoding:
            encodings = [
                e.strip()
                for e in content_encoding.split(",")
                if e.strip() in self.CONTENT_DECODERS
            ]
            if len(encodings):
                self._decoder = _get_decoder(content_encoding)

    def _process_headers(self, headers):
        ctype = ContentType.PLAIN
        decoder = None
        ret = {}
        for key, value in headers.items():
            if key.upper() == "CONTENT-TYPE":
                if self.json_re.match(value):
                    ctype = ContentType.JSON
                elif self.form_re.match(value):
                    ctype = ContentType.FORM
                elif not self.non_binary_re.match(value):
                    ctype = ContentType.BINARY

            if key.upper() == "CONTENT-ENCODING":
                decoder = self._init_decoder(value)

            if self._is_filtered_key(key):
                ret[key] = FILTERED
                continue
            ret[key] = self._sanitize_value(value)

        return ret, ctype, decoder

    def _decode_body(self, data, decoder):
        if decoder is None:
            return data.getvalue()

        try:
            decompressed = decoder.decompress(data.getvalue())
            return decompressed
        except self.DECODER_ERROR_CLASSES:
            return data.getvalue()

    def _process_body(self, body, ctype, decoder):
        body_bytes = self._decode_body(body, decoder)
        if len(body_bytes) > self.MAX_BODY_SIZE:
            return "(omitted due to size)"

        body = body_bytes.decode()
        if ctype == ContentType.JSON:
            try:
                body = json.dumps(self._sanitize_value(json.loads(body)))
            except TypeError:
                pass
        elif ctype == ContentType.FORM:
            try:
                body = urllib.parse.urlencode(
                    self._sanitize_value(urllib.parse.parse_qs(body)), doseq=True
                )
            except (ValueError, TypeError):
                pass
        elif ctype == ContentType.BINARY:
            body = "(not showing binary data)"
        else:
            body = self._sanitize_value(body)

        return body

    def _process_url(self, log):
        hostname = log["hostname"]
        port = log["port"]
        protocol = log["protocol"]

        include_port = (protocol == "https" and port != 443) or (
            protocol == "http" and port != 80
        )
        port_str = f":{port}" if include_port else ""

        path = "/".join(
            urllib.parse.quote(self._sanitize_value(urllib.parse.unquote(segment)))
            for segment in log["path"].split()
        )

        params = self._sanitize_value(log["params"])
        params_str = (
            f"?{urllib.parse.urlencode(params, doseq=True)}" if len(params) != 0 else ""
        )

        url = f"{protocol}://{hostname}{port_str}{path}{params_str}"

        log.update({"url": url, "params": params, "path": path})

    def run(self, report):
        self._process_url(report)

        request_headers, req_ctype, req_decoder = self._process_headers(
            report["requestHeaders"]
        )
        request_body = self._process_body(report["requestBody"], req_ctype, req_decoder)

        response_headers, resp_ctype, resp_decoder = self._process_headers(
            report["responseHeaders"]
        )
        response_body = self._process_body(
            report["responseBody"], resp_ctype, resp_decoder
        )

        report.update(
            {
                "requestHeaders": request_headers,
                "requestBody": request_body,
                "responseHeaders": response_headers,
                "responseBody": response_body,
            }
        )
        return report
