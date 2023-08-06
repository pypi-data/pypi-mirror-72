# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

import logging

from .config import DynamicConfig


class Matcher(object):
    def __init__(self, cfg):
        self.cfg = cfg
        self.logger = logging.getLogger("bearer")

    def run(self, log):
        filters = self.cfg.filters
        active_rules = []
        config = {}

        def add_rule(rule):
            active_rules.append(rule.summary)
            config.update(rule.config)

        for rule in self.cfg.data_collection_rules:
            if rule.filter_hash is None:
                add_rule(rule)
                continue

            filter_ = filters.get(rule.filter_hash, None)
            if filter_ is None:
                self.logger.debug(
                    "ignoring rule with unknown filter hash %s", rule.filter_hash
                )
                continue

            matches = filter_.match(log, filters)
            self.logger.debug("filter %s match=%s", rule.filter_hash, matches)
            if matches:
                add_rule(rule)

        return Result(active_rules, DynamicConfig(self.cfg, config))


class Result:
    def __init__(self, active_rules, config):
        self.active_rules = active_rules
        self.config = config
