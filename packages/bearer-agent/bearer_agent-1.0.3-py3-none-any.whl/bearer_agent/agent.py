# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

from collections import deque
import logging
import atexit

from .config import ConfigOptions, setup_hooks
from .errors import error_safe
from .remote_config import ConfigFetcher
from .report_consumer import ReportConsumer

MAX_REPORTS = 1000


class AgentState(object):
    LINKED = 1
    UNLINKED = 2


class Agent(object):
    """
    The Bearer_ agent helps you monitor HTTP requests on your application.
    """

    __HOOKS_SETUP__ = False

    def __init__(self):
        self.cfg = ConfigOptions()
        self.user_cfg = None
        # don't lock or wait when adding a new report,
        # instead we discard older reports. also enqueue is thread safe.
        self.queue = deque(maxlen=MAX_REPORTS)
        self.consumer = None
        self.config_fetcher = None
        self.log = logging.getLogger("bearer")

    def init(self, **user_cfg):
        with error_safe():
            if self.user_cfg == user_cfg:
                return

            self.user_cfg = user_cfg.copy()
            # init config
            for k, v in user_cfg.items():
                if k not in self.cfg.options:
                    continue
                self.cfg.set(k, v)

            if self.cfg.disabled:
                self.log.warn("agent is disabled, API calls will not be monitored")
                return

            if not self.cfg.secret_key:
                self.log.warn(
                    "missing Bearer secret key, API calls will not be monitored. "
                    "Please set the secret_key configuration option to enable the agent"
                )
                return

            self.setup_hooks()

            if self.cfg.nolink:
                return

            self.link_service()

    def setup_hooks(self):
        # don't patch twice
        if self.__HOOKS_SETUP__:
            return

        self.log.info("installing HTTP interceptors")
        setup_hooks(self.cfg)
        self.__HOOKS_SETUP__ = True

    def is_disabled(self):
        return self.cfg.disabled

    def enqueue_report(self, report):
        self.log.debug("enqueue report")
        self.queue.append(report)

    def dequeue_report(self):
        return self.queue.popleft()

    def pending(self):
        return len(self.queue)

    def link_service(self):
        if self.config_fetcher is None:
            self.config_fetcher = ConfigFetcher(cfg)
            self.config_fetcher.start()

        if self.consumer is None:
            self.consumer = ReportConsumer(self, cfg)
            self.consumer.start()

    def unlink_service(self):
        if self.consumer is not None:
            self.consumer.stop()
            self.consumer = None

        if self.config_fetcher is not None:
            self.config_fetcher.stop()
            self.config_fetcher = None


agent = Agent()

init = agent.init
enqueue_report = agent.enqueue_report
dequeue_report = agent.dequeue_report
is_disabled = agent.is_disabled
link_service = agent.link_service
unlink_service = agent.unlink_service
pending = agent.pending
cfg = agent.cfg

atexit.register(unlink_service)
