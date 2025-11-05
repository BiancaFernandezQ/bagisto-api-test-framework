from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

BASE_URI = os.getenv("BASE_URI", "http://localhost:8000/api/v1")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
DEVICE_NAME = os.getenv("DEVICE_NAME")


REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "25"))