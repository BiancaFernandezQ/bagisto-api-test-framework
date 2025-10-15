import os
import requests
import pytest

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000/api/v1")

ADMIN_EMAIL =  "admin@example.com"
ADMIN_PASSWORD = "admin123"
DEVICE_NAME = "ci-test"


@pytest.fixture(scope="session")
def get_token():
    """
    Hace login y obtiene un token válido para las pruebas.
    """
    login_url = f"{BASE_URL}/admin/login"
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


def test_get_admin_customers(get_token):
    """
    Valida el listado de clientes en Bagisto Admin usando el token obtenido dinámicamente.
    """
    url = f"{BASE_URL}/admin/customers"
    headers = {
        "Authorization": f"Bearer {get_token}"
    }

    response = requests.get(url, headers=headers)

    print("Status:", response.status_code)
    print("Response text:", response.text[:500])

    assert response.status_code == 200, f"Status inesperado: {response.status_code}"
    json_data = response.json()

    assert isinstance(json_data, dict), "La respuesta no es un JSON válido"
    assert "data" in json_data, "No se encontró el campo 'data'"
    print(f"Clientes retornados: {len(json_data['data'])}")
