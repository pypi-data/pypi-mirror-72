# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from .base import FilterType, KeyValueFilterBase


class RequestHeaderFilter(KeyValueFilterBase):
    type_name = FilterType.RequestHeaderFilter

    def match(self, log, filters):
        if "requestHeaders" not in log:
            return False
        return self._match(log["requestHeaders"])
