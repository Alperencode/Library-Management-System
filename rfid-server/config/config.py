from dotenv import load_dotenv, find_dotenv
from internal.utils.ip import get_local_ip
from internal.utils.logger import logger
import sys
import os

dotenv_path = find_dotenv(filename="../.env")
if not dotenv_path:
    logger.warning(".env file not found. Exiting program.")
    sys.exit(1)

LOCAL_IP = get_local_ip()
conf = {}

load_dotenv(override=True)

required_envs = {
    "algorithm": os.getenv("ALGORITHM"),
    "secret_key": os.getenv("SECRET_KEY"),
    "environment": os.getenv("ENVIRONMENT"),
}

missing_keys = [key for key, value in required_envs.items() if not value]
if missing_keys:
    logger.error(f"Missing required environment variables: {', '.join(missing_keys)}. Exiting program.")
    sys.exit(1)

conf.update(required_envs)


def get_config(name):
    if name == "all":
        return conf
    return conf[name]


def set_config(name, value):
    conf[name] = value
