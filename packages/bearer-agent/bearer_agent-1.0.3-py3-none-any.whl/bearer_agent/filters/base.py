# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from ..util import flag

import re

KNOWN_FILTERS = []


class FilterType(object):

    DomainFilter = "DomainFilter"
    StatusCodeFilter = "StatusCodeFilter"
    ConnectionErrorFilter = "ConnectionErrorFilter"
    FilterSet = "FilterSet"
    PathFilter = "PathFilter"
    HttpMethodFilter = "HttpMethodFilter"
    ParamFilter = "ParamFilter"
    RequestHeaderFilter = "RequestHeaderFilter"
    ResponseHeaderFilter = "ResponseHeaderFilter"
    NotFilter = "NotFilter"


class FilterMeta(type):
    def __new__(cls, name, bases, attrs):
        super_new = super().__new__
        parents = [b for b in bases if isinstance(b, FilterMeta)]
        if not parents:
            return super_new(cls, name, bases, attrs)
        new_class = super_new(cls, name, bases, attrs)
        KNOWN_FILTERS.append(new_class)
        return new_class


class Filter(object):
    type_name = None

    def __init__(self, filter_dict):
        self.filter_dict = filter_dict

    def match(self, log, filters):
        raise NotImplementedError


Filter = FilterMeta("Filter", (Filter,), {})


class RegularExpression(object):
    def __init__(self, value, flags=None):
        self.value = (value,)
        self.flags = flags
        self._regexp = re.compile(value, flag(flags))

    def match(self, string):
        if self._regexp.search(string):
            return True

        return False


class Range(object):
    def __init__(self, start, end=None):
        self.start = start
        # if no end given , set it to start
        self.end = end or start

    def match(self, code):
        return self.start <= code <= self.end


class KeyValueFilterBase(Filter):
    def __init__(self, filter_dict):
        super().__init__(filter_dict)

        value_pattern_dict = filter_dict.get("valuePattern")
        key_pattern_dict = filter_dict.get("keyPattern")
        self.value_pattern = (
            RegularExpression(**value_pattern_dict) if value_pattern_dict else None
        )
        self.key_pattern = (
            RegularExpression(**key_pattern_dict) if key_pattern_dict else None
        )

    def _match(self, d):
        for key, val in d.items():
            key_matches = not self.key_pattern or self.key_pattern.match(key)
            value_matches = not self.value_pattern or self.value_pattern.match(val)

            if key_matches and value_matches:
                return True
        return False
