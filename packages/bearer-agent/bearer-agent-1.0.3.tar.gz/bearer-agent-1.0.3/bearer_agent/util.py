# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

import io
import time
import re
import base64
import platform

import pkg_resources
import wrapt

__version__ = pkg_resources.get_distribution("bearer-agent").version
version_info = tuple(int(v) for v in __version__.split("."))


def reraise(tp, value, tb=None):
    try:
        if value is None:
            value = tp()
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value
    finally:
        value = None
        tb = None


def current_time():
    return int(round(time.time() * 1000))


def flag(flag_str):
    flags = 0

    if not flag_str:
        return flags

    for flag in flag_str:
        attr_name = flag.upper()
        if not hasattr(re, attr_name):
            raise ValueError(f"invalid flag {flag}")
        flags = flags | getattr(re, attr_name)

    return flags


def _is_text_io(stream):
    """Test whether a file-like object is a text or a binary stream.
    """
    return isinstance(stream, io.TextIOBase)


def encode_environment(environment):
    return base64.b64encode(environment.encode("utf8")).decode("utf8")


def runtime_env():
    return {
        "arch": platform.machine(),
        "hostname": platform.node() or "unknown",
        "type": platform.system(),
        "platform:": platform.platform(),
        "version": platform.python_version(),
    }


def agent_env():
    return {"type": "python", "version": __version__}


class ReadProxy(wrapt.ObjectProxy):

    __target__ = None

    def __init__(self, wrapped, target):
        super().__init__(wrapped)
        self.__encode = _is_text_io(wrapped)
        self.__target__ = target

    def read(self, amt=None):
        data = self.__wrapped__.read(amt)
        if self.__encode:
            self.__target__.write(data.encode("utf-8"))
        else:
            if isinstance(data, str):
                self.__target__.write(data.encode("utf-8"))
            else:
                self.__target__.write(data)
        return data


class BufferProxy(wrapt.ObjectProxy):

    __target__ = None

    def __init__(self, wrapped, target):
        super().__init__(wrapped)
        self.__target__ = target

    def __iter__(self):
        it = iter(self.__wrapped__)
        for chunk in it:
            if isinstance(chunk, str):
                self.__target__.write(chunk.encode("utf-8"))
            else:
                self.__target__.write(chunk)
            yield chunk


class AsyncReadProxy(wrapt.ObjectProxy):

    __target__ = None

    def __init__(self, wrapped, target):
        super().__init__(wrapped)
        self.__target__ = target

    async def read(self):
        data = await self.__wrapped__.read()
        if isinstance(data, str):
            self.__target__.write(data.encode("utf-8"))
        else:
            self.__target__.write(data)
        return data
