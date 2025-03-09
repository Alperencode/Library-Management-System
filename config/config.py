from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

VERSION = "v0.1.0"
Health = False
Ready = False

conf = {}

# API Configuration
conf["api_port"] = int(os.environ.get("API_PORT", "8000"))
conf["api_prefix"] = os.environ.get("API_PREFIX", "/api/v1")
conf["algorithm"] = os.environ.get("ALGORITHM", "")
conf["access_token_expire_minutes"] = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
conf["refresh_token_expire_days"] = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
conf["secret_key"] = os.getenv("SECRET_KEY")

# MongoDB Configuration
conf["mongodb_user"] = os.environ.get("MONGODB_USERNAME", "")
conf["mongodb_pass"] = os.environ.get("MONGODB_PASSWORD", "")
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
