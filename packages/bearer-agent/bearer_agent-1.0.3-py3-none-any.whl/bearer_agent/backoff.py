# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.

import time
import random


class FixedBackoff(object):
    def __init__(self, delay):
        self.delay = delay

    def next(self):
        return self.delay

    def sleep(self):
        time.sleep(self.delay)


class ExponentialBackoff(object):
    def __init__(self, min_delay, max_delay, step):
        if min_delay >= max_delay:
            raise ValueError("max_delay must be greater than min_delay")

        if min_delay <= 0 or step <= 0:
            raise ValueError("min_delay or step must be greater than 0")

        self.min_delay = min_delay
        self.max_delay = max_delay
        self.step = step

    def next(self, attempts):
        multiple = attempts >> 1
        curr_max = max(self.min_delay + self.step * multiple, self.max_delay)
        return int(random.uniform(self.min_delay, curr_max))

    def sleep(self, attempts):
        time.sleep(self.next(attempts))
