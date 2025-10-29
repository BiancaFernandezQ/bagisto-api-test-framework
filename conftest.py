import pytest
import requests
from config.config import BASE_URI, ADMIN_EMAIL, ADMIN_PASSWORD, DEVICE_NAME

@pytest.fixture(scope="session")
def get_token():
    #login, obtener token y retornarlo
    login_url = f"{BASE_URI}/admin/login"
    payload = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD,
        "device_name": DEVICE_NAME
    }

    response = requests.post(login_url, json=payload)
    assert response.status_code == 200, f"Error al hacer login: {response.text}"

    token = response.json().get("token")
    print("Token obtenido:", token)
    assert token, "No se recibió token en la respuesta"
    return token
