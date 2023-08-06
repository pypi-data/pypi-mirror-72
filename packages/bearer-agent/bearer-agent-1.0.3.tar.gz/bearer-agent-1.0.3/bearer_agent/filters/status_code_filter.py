# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from .base import FilterType, Filter, Range


class StatusCodeFilter(Filter):
    type_name = FilterType.StatusCodeFilter

    def __init__(self, filter_dict):
        super().__init__(filter_dict)

        range_dict = filter_dict["range"]
        start = range_dict["from"]
        end = range_dict["to"]
        self.range = Range(start, end)

    def match(self, log, filters):
        status_code = log["statusCode"]
        return self.range.match(status_code) if status_code else False
