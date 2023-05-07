from os.path import join, dirname

from dotenv import load_dotenv
from utils.env_loader import load_env

dotenv_path = join(dirname(__file__), "./", ".env")
load_dotenv(dotenv_path)

APP_NAME = load_env("APP_NAME", "payhere-test")

# Logger
LOG_DIR = load_env("LOG_DIRECTORY", "./logs")
LOG_LEVEL = load_env("LOG_LEVEL", "DEBUG")

# DB
MYSQL_HOST = load_env("MYSQL_HOST", required=True)
MYSQL_DB_NAME = load_env("MYSQL_DB_NAME", required=True)
MYSQL_PORT = load_env("MYSQL_PORT", "3306", as_type=int)
MYSQL_USER = load_env("MYSQL_USER", required=True)
MYSQL_PASSWORD = load_env("MYSQL_PASSWORD", required=True)

# Django Secret Key
DJANGO_SECRET_KEY = load_env("DJANGO_SECRET_KEY", required=True)

# Auth
ACCESS_TOKEN_LIFETIME = load_env("ACCESS_TOKEN_LIFETIME", str(60 * 60), required=True, as_type=int)
REFRESH_TOKEN_LIFETIME = load_env("ACCESS_TOKEN_LIFETIME", str(24 * 60 * 60), required=True, as_type=int)
