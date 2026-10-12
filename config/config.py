import os
from pathlib import Path

from dotenv import load_dotenv

ENV_FILE = Path(__file__).with_name(".env")
load_dotenv(ENV_FILE)

BASE_URL = os.getenv("BASE_URL", "https://ru.yougile.com/api-v2")
API_TOKEN = os.getenv("API_TOKEN", "")
UI_BASE_URL = os.getenv("UI_BASE_URL", "https://ru.yougile.com")
UI_EMAIL = os.getenv("UI_EMAIL", "")
UI_PASSWORD = os.getenv("UI_PASSWORD", "")
