import os


VERSION = "v0.1.0"
Health = False
Ready = False

conf = {}

api_port = os.environ.get("API_PORT", 8000)
api_prefix = os.environ.get("API_PREFIX", "/api/v1")


conf["health"] = Health
conf["ready"] = Ready
conf["api_port"] = api_port
conf["api_prefix"] = api_prefix


def get_config(name):
    if name == "all":
        return conf
    return conf[name]


def set_config(name, value):
    conf[name] = value


def append_conf(name, value):
    conf[name].append(value)
