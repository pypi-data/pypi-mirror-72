# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from threading import Event, Thread
import time
import logging
import traceback

from .config import LOG_LEVELS, DETECTED, RESTRICTED
from .util import agent_env, encode_environment, runtime_env
from .client import Client
from .sanitize import Sanitizer
from .matcher import Matcher


DETECTED_KEYS = ["hostname", "logLevel", "protocol", "port"]
RESTRICTED_DROP_KEYS = [
    "requestHeaders",
    "responseHeaders",
    "requestBody",
    "responseBody",
]


class ReportConsumer(Thread):

    report_template = {}

    def __init__(self, agent, cfg):
        super().__init__()
        self.daemon = True
        self.agent = agent
        self._stop_ev = Event()
        self._stopped_ev = Event()
        self.cfg = cfg
        self.client = Client(cfg)
        self.sanitizer = Sanitizer(cfg)
        self.matcher = Matcher(cfg)
        self._init_template()
        self.logger = logging.getLogger("bearer")

    def stop(self):
        self.logger.debug(
            "stopping report consumer. waiting for %i outstanding report(s)",
            self.agent.pending(),
        )
        self._stop_ev.set()
        self._stopped_ev.wait()

    def run(self):
        try:
            while not self._stop_ev.is_set() or self.agent.pending():
                self.cfg.await_update()

                try:
                    log_report = self.agent.dequeue_report()
                except IndexError:
                    time.sleep(0.1)
                    continue

                self.logger.debug("sending report")

                try:
                    self._handle_log(log_report)
                except Exception:
                    self.logger.error("error sending report:")
                    self.logger.error(traceback.format_exc())
        finally:
            self._stopped_ev.set()

    def _init_template(self):
        self.report_template = {
            "secretKey": self.cfg.secret_key,
            "runtime": runtime_env(),
            "agent": agent_env(),
            "logs": [],
            "appEnvironment": encode_environment(self.cfg.environment),
        }

    def _handle_log(self, log_report):
        log = log_report.process()
        matcher_result = self.matcher.run(log)

        if not matcher_result.config.active:
            self.logger.debug("API deactivated in Dashboard, ignoring API")
            return

        log_level = matcher_result.config.log_level
        log["logLevel"] = LOG_LEVELS[log_level]

        if log_level == DETECTED:
            log = {key: log[key] for key in DETECTED_KEYS}
        else:
            log["activeDataCollectionRules"] = matcher_result.active_rules

            if log_level == RESTRICTED:
                for key in RESTRICTED_DROP_KEYS:
                    del log[key]
            else:
                if self.cfg.strip_sensitive_data:
                    log = self.sanitizer.run(log)

        report = self.report_template.copy()
        report["logs"] = [log]
        self.client.send_report(report)
