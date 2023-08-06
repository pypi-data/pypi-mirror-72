# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

import http.client as client
import logging
import json
import socket

from .backoff import ExponentialBackoff
from .util import agent_env, encode_environment, runtime_env


class Client(object):

    CONFIG_PATH = "/config"
    REPORT_PATH = "/logs"

    def __init__(self, cfg):
        self.cfg = cfg
        # we sleep max 5 secs, min 200ms and step by 200ms
        self.backoff = ExponentialBackoff(0.2, 5, 0.2)
        self.logger = logging.getLogger("bearer")

    def fetch_config(self):
        headers = {
            "Authorization": self.cfg.secret_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        body = json.dumps(
            {
                "agent": agent_env(),
                "application": {
                    "environment": encode_environment(self.cfg.environment)
                },
                "runtime": runtime_env(),
            }
        )

        h = client.HTTPSConnection(self.cfg.config_host)
        h._bearer_disabled = True
        attempts = 1
        while True:
            try:
                h.request("POST", self.CONFIG_PATH, body=body, headers=headers)
                resp = h.getresponse()
                json_body = resp.read().decode()
                self.logger.debug("remote config received: %s", json_body)
                return json.loads(json_body)
            except (client.HTTPException, socket.error) as exc:
                self.logger.error("retrying fetching config: %s", str(exc))
                self.backoff.sleep(attempts)
                attempts += 1
            finally:
                h.close()

    def send_report(self, report):
        headers = {"Content-Type": "application/json"}
        attempts = 1
        while True:
            h = client.HTTPSConnection(self.cfg.report_host)
            h._bearer_disabled = True
            body = json.dumps(report)
            self.logger.debug("sending report: %s", body)

            try:
                h.request("POST", self.REPORT_PATH, body=body, headers=headers)
                resp = h.getresponse()
                json_body = resp.read().decode()
                return json.loads(json_body)
            except (client.HTTPException, socket.error) as exc:
                self.logger.error("retrying sending report: %s", str(exc))
                self.backoff.sleep(attempts)
                attempts += 1
            finally:
                h.close()
