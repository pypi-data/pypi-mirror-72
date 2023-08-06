# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from .base import FilterType, Filter, RegularExpression


class PathFilter(Filter):
    type_name = FilterType.PathFilter

    def __init__(self, filter_dict):
        super().__init__(filter_dict)

        if "pattern" not in filter_dict:
            raise TypeError("invalid domain filter")

        self.pattern = RegularExpression(**filter_dict["pattern"])

    def match(self, log, filters):
        if "path" not in log:
            return False
        return self.pattern.match(log["path"])
