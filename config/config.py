import os
from internal.utils.utils import get_secret_key

VERSION = "v0.1.0"
Health = False
Ready = False

conf = {}

conf["api_port"] = int(os.environ.get("API_PORT", "8000"))
conf["api_prefix"] = os.environ.get("API_PREFIX", "/api/v1")
conf["algorithm"] = os.environ.get("ALGORITHM", "HS256")
conf["access_token_expire_minutes"] = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
conf["refresh_token_expire_days"] = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
conf["secret_key"] = get_secret_key(".env")


def get_config(name):
    if name == "all":
        return conf
    return conf[name]


def set_config(name, value):
    conf[name] = value


def append_conf(name, value):
    conf[name].append(value)
