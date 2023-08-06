# -*- coding: utf-8 -
#
# This file is part of bearer-agent released under the Apache License 2.
# See the NOTICE for more information.


import copy
import re
import textwrap
import threading

import wrapt

from .errors import ConfigError
from .filters import FILTERS_BY_NAME

if hasattr(re, "Pattern"):
    from re import Pattern
else:
    import sre_compile
    Pattern = type(sre_compile.compile("", 0))

KNOWN_OPTIONS = []

# define log levels
DETECTED = 0
RESTRICTED = 1
ALL = 2

LOG_LEVELS = {ALL: "ALL", RESTRICTED: "RESTRICTED", DETECTED: "DETECTED"}

LOG_LEVELS_BY_STRING = dict([(val, key) for key, val in LOG_LEVELS.items()])


def make_options(ignore=None):
    options = {}
    ignore = ignore or ()
    for o in KNOWN_OPTIONS:
        opt = o()
        if opt.name in ignore:
            continue
        options[opt.name] = opt.copy()
    return options


class ConfigOptions(object):
    """ OPTIONS """

    def __init__(self):
        self.options = make_options()
        self._update_ev = threading.Event()

    def __getattr__(self, name):
        if name not in self.options:
            raise AttributeError("No configuration option for: %s" % name)
        return self.options[name].get()

    def __setattr__(self, name, value):
        if name != "options" and name in self.options:
            raise AttributeError("Use .set(...) to set configuration options")
        super().__setattr__(name, value)

    def set(self, name, value):
        if name not in self.options:
            raise AttributeError("No configuration option for: %s" % name)
        self.options[name].set(value)

    def notify_update(self):
        self._update_ev.set()

    def begin_update(self):
        self._update_ev.clear()

    def await_update(self, timeout=None):
        if self.nolink:
            return
        self._update_ev.wait(timeout)

    def dumps(self):
        d = {}
        for name in self.options:
            val = self.options[name].get()
            if name == "log_level":
                val = LOG_LEVELS[val]
            d[name] = val
        return d


class ConfigUpdate(object):
    def __init__(self, cfg):
        self.cfg = cfg

    def __enter__(self):
        self.cfg.begin_update()

    def __exit__(self, *args):
        self.cfg.notify_update()


def _import_module_hook(name, function="intercept"):
    return name + ":" + function


def setup_hooks(cfg):
    wrapt.register_post_import_hook(
        _import_module_hook("bearer_agent.hooks.intercept_urllib3"), "urllib3"
    )

    wrapt.register_post_import_hook(
        _import_module_hook("bearer_agent.hooks.intercept_http"), "http.client"
    )

    wrapt.register_post_import_hook(
        _import_module_hook("bearer_agent.hooks.intercept_aiohttp"), "aiohttp"
    )


class OptionMeta(type):
    def __new__(cls, name, bases, attrs):
        super_new = super().__new__
        parents = [b for b in bases if isinstance(b, OptionMeta)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        attrs["order"] = len(KNOWN_OPTIONS)
        attrs["validator"] = staticmethod(attrs["validator"])

        new_class = super_new(cls, name, bases, attrs)
        new_class.fmt_desc(attrs.get("desc", ""))
        KNOWN_OPTIONS.append(new_class)
        return new_class

    def fmt_desc(cls, desc):
        desc = textwrap.dedent(desc).strip()
        setattr(cls, "desc", desc)
        setattr(cls, "short", desc.splitlines()[0])


class Option(object):
    name = None
    value = None
    order = 0
    validator = None
    required = None
    default = None
    short = None
    desc = None

    def __init__(self):
        if self.default is not None:
            self.set(self.default)

    def copy(self):
        return copy.copy(self)

    def get(self):
        return self.value

    def set(self, val):
        if not callable(self.validator):
            raise TypeError("Invalid validator: %s" % self.name)
        self.value = self.validator(val)

    def __lt__(self, other):
        return self.order < other.order

    __cmp__ = __lt__

    def __repr__(self):
        return "<%s.%s object at %x with value %r>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            id(self),
            self.value,
        )


Option = OptionMeta("Option", (Option,), {})


class DynamicConfig(object):
    def __init__(self, cfg, dynamic_cfg):
        log_level = dynamic_cfg.get("logLevel")
        self.log_level = LOG_LEVELS_BY_STRING[log_level] if log_level else cfg.log_level
        self.active = dynamic_cfg.get("active", True)


class DataCollectionRule(object):
    def __init__(self, rule):
        self.filter_hash = rule.get("filterHash", None)
        self.params = rule.get("params", None)
        self.config = rule.get("config", {})
        self.signature = rule.get("signature", "")

    @property
    def summary(self):
        return {
            "filterHash": self.filter_hash,
            "params": self.params,
            "signature": self.signature,
        }


def validate_bool(val):
    if val is None:
        return None
    if isinstance(val, bool):
        return val
    else:
        raise ConfigError("Invalid boolean: %s" % val)


def validate_string(val):
    if val is None:
        return None
    if not isinstance(val, str):
        raise ConfigError("Not a string: %s" % val)
    return val.strip()


def validate_secret_key(val):
    val = validate_string(val)
    if not val:
        raise ConfigError("secret key is  empty")
    return val


def validate_list_string(val):
    if not val:
        return []
    if isinstance(val, str):
        val = [val]
    return [validate_string(v) for v in val]


def validate_loglevel(val):
    if not isinstance(val, int):
        if isinstance(val, str):
            if val in LOG_LEVELS_BY_STRING:
                return LOG_LEVELS_BY_STRING[val]
        raise ConfigError("Invalid log level: %s" % val)
    if 0 <= val <= 2:
        return val
    raise ConfigError("Not an a log level: %s" % val)


def validate_regexp(value):
    if isinstance(value, Pattern):
        return value

    if not isinstance(value, str):
        raise ConfigError("Not a string: %s", value)

    return re.compile(value, re.I)


def validate_data_collection_rules(collection):
    if not isinstance(collection, list):
        raise TypeError("invalid data collection rules")

    rules = []
    for rule in collection:
        rules.append(DataCollectionRule(rule))

    return rules


def validate_filters(filters):
    if not isinstance(filters, dict):
        raise TypeError("invalid filters")

    filter_initialized = {}
    for hkey, filter_dict in filters.items():
        type_name = filter_dict["typeName"]
        if type_name not in FILTERS_BY_NAME:
            raise ValueError("unknown filter")

        try:
            cls = FILTERS_BY_NAME[type_name]
            obj = cls(filter_dict)
            filter_initialized[hkey] = obj
        except Exception:
            raise ValueError("invalid filter")

    return filter_initialized


def validate_environment(environment):
    environment = validate_string(environment)
    return environment.lower() if environment else None


class NoLink(Option):
    name = "nolink"
    validator = validate_bool
    default = False
    desc = """\
        do not link to the bearer API if set.
        """


class Disabled(Option):
    name = "disabled"
    validator = validate_bool
    default = False
    desc = """\
        When set, the Bearer agent is disabled.

        .. versionadded:: 0.0.1
        """


class Environment(Option):
    name = "environment"
    validator = validate_environment
    default = "default"
    desc = """\
        You application's envionment name.
        """


class SecretKey(Option):
    name = "secret_key"
    validator = validate_secret_key
    default = None
    desc = """\
        Required, string: Your Bearer private key

        .. versionadded:: 0.0.1
        """


class Ignored(Option):
    name = "ignored"
    validator = validate_list_string
    default = []
    desc = """\
        An array of domains you do not want monitored by the Agent

        .. versionadded:: 0.0.1
        """


class LogLevel(Option):
    name = "log_level"
    validator = validate_loglevel
    default = DETECTED
    desc = """\
        Set the level of information you want the agent to gather. Valid values
        are ALL (to send full request and response), RESTRICTED (to send only
        the path and query string), or DETECTED (to send only hostname, protocol
        and port).

        .. versionadded:: 0.0.1
        """


class ConfigHost(Option):
    name = "config_host"
    validator = validate_string
    default = "config.bearer.sh"
    desc = """\
        Host where to retrieve the user configuration
        """


class ReportHost(Option):
    name = "report_host"
    validator = validate_string
    default = "agent.bearer.sh"
    desc = """\
        Host where to send the lois
        """


class StripSensitiveData(Option):
    name = "strip_sensitive_data"
    default = True
    validator = validate_bool
    desc = """\
        strip sensitive data
        """


class StripSensitiveRegex(Option):
    name = "strip_sensitive_regex"
    validator = validate_regexp
    default = re.compile(
        "|".join(
            [
                r"[a-zA-Z0-9]{1}[a-zA-Z0-9.!#$%&’*+=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*",
                r"(?:\d[ -]*?){13,16}",
            ]
        ),
        re.I,
    )
    desc = """\
        sensitive data regexp
        """


class StripSensitiveKeys(Option):
    name = "strip_sensitive_keys"
    validator = validate_regexp
    default = re.compile(
        "|".join(
            [
                "^authorization$",
                "^password$",
                "^secret$",
                "^passwd$",
                "^api.?key$",
                "^access.?token$",
                "^auth.?token$",
                "^credentials$",
                "^mysql_pwd$",
                "^stripetoken$",
                "^card.?number.?$",
                "^secret$",
                "^client.?id$",
                "^client.?secret$",
            ]
        ),
        re.I,
    )
    desc = """\
        sensitive keys regexp
        """


class Filters(Option):
    name = "filters"
    validator = validate_filters
    default = {}
    desc = """\
        map associating filters records to their hash
        """


class DataCollectionRules(Option):
    name = "data_collection_rules"
    validator = validate_data_collection_rules
    default = []
    desc = """\
        list of rules to filter a request or response
        """
