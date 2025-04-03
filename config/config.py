from dotenv import load_dotenv, find_dotenv
from internal.utils.logger import logger
import os
import sys

# Check if .env exists
dotenv_path = find_dotenv()
if not dotenv_path:
    logger.warning(".env file not found. Exiting program.")
    sys.exit(1)

# Load .env file
load_dotenv(override=True)

VERSION = "v0.1.0"
Health = False
Ready = False

conf = {}

# API Configuration
conf["api_port"] = int(os.environ.get("API_PORT", "8000"))
conf["api_prefix"] = os.environ.get("API_PREFIX", "/api/v1")
conf["access_token_expire_minutes"] = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
conf["refresh_token_expire_days"] = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Required variables
required_envs = {
    "algorithm": os.getenv("ALGORITHM"),
    "secret_key": os.getenv("SECRET_KEY"),
    "environment": os.getenv("ENVIRONMENT"),
    "email_host": os.getenv("EMAIL_HOST"),
    "email_port": os.getenv("EMAIL_PORT"),
    "email_username": os.getenv("EMAIL_USERNAME"),
    "email_password": os.getenv("EMAIL_PASSWORD"),
}

# Check required variables
missing_keys = [key for key, value in required_envs.items() if not value]
if missing_keys:
    logger.error(f"Missing required environment variables: {', '.join(missing_keys)}. Exiting program.")
    sys.exit(1)

# Assign required variables to config
conf.update(required_envs)
conf["email_port"] = int(conf["email_port"])

# MongoDB Configuration
conf["mongodb_user"] = os.getenv("MONGODB_USERNAME")
conf["mongodb_pass"] = os.getenv("MONGODB_PASSWORD")
conf["mongodb_host"] = os.environ.get("MONGODB_HOST", "127.0.0.1:27017")
conf["mongodb_database"] = os.environ.get("MONGODB_DATABASE", "library_management_system")

if conf["mongodb_user"] and conf["mongodb_pass"]:
    conf["mongodb_uri"] = f'mongodb+srv://{conf["mongodb_user"]}:{conf["mongodb_pass"]}@{conf["mongodb_host"]}'
else:
    conf["mongodb_uri"] = f'mongodb://{conf["mongodb_host"]}/{conf["mongodb_database"]}'


def get_config(name):
    if name == "all":
        return conf
    return conf[name]


def set_config(name, value):
    conf[name] = value
