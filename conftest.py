import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "http://localhost:9000/api")

@pytest.fixture(scope="session")
def admin_token(base_url):
    payload = {
        "email": os.getenv("ADMIN_EMAIL"),
        "password": os.getenv("ADMIN_PASSWORD")
    }
    response = requests.post(f"{base_url}/admin/login", json=payload)
    response.raise_for_status()
    return response.json()["token"]
