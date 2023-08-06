# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from .base import KNOWN_FILTERS

from .connection_error_filter import ConnectionErrorFilter
from .domain_filter import DomainFilter
from .status_code_filter import StatusCodeFilter
from .path_filter import PathFilter
from .http_method_filter import HttpMethodFilter
from .filterset import FilterSet
from .request_header_filter import RequestHeaderFilter
from .response_header_filter import ResponseHeaderFilter
from .param_filter import ParamFilter
from .not_filter import NotFilter

FILTERS_BY_NAME = dict([(cls.type_name, cls) for cls in KNOWN_FILTERS])

__ALL__ = [
    ConnectionErrorFilter,
    DomainFilter,
    StatusCodeFilter,
    PathFilter,
    HttpMethodFilter,
    RequestHeaderFilter,
    ResponseHeaderFilter,
    ParamFilter,
    NotFilter,
    FilterSet,
    KNOWN_FILTERS,
    FILTERS_BY_NAME,
]
