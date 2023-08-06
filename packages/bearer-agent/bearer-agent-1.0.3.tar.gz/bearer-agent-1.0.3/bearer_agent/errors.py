# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

import contextlib
import logging
import traceback


logger = logging.getLogger("bearer")


class ErrorBase(Exception):
    pass


class ConfigError(ErrorBase):
    """ Exception raised on config error """


@contextlib.contextmanager
def error_safe():
    try:
        yield
    except ErrorBase:
        logger.error(traceback.format_exc())
    except Exception:
        logger.error(
            "An unexpected error has occured. Please email us at support+python_agent@bearer.sh for support."
        )
        logger.error(traceback.format_exc())
