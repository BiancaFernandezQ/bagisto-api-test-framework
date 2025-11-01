import pytest
import requests
from config.config import ADMIN_EMAIL, ADMIN_PASSWORD, DEVICE_NAME
from src.bagisto_api.endpoint import Endpoint
from src.helpers.customer_helper import CustomerHelper
from src.helpers.groups_helper import GroupHelper

@pytest.fixture(scope="session")
def get_token():
    #login, obtener token y retornarlo
    login_url = Endpoint.BASE_LOGIN.value
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

@pytest.fixture(scope="session")
def create_15_customers(get_token):
    responses = CustomerHelper.create_multiple_random_customers(get_token, 15)
    for i, response in enumerate(responses):
        assert response.status_code == 200, f"Fallo al crear el cliente #{i+1}. Status: {response.status_code}, Body: {response.text}"
    return responses

@pytest.fixture(scope="session")
def create_5_groups(get_token):
    responses = GroupHelper.create_multiple_random_groups(get_token, 5)
    for i, response in enumerate(responses):
        assert response.status_code == 200, f"Fallo al crear el grupo #{i+1}. Status: {response.status_code}, Body: {response.text}"
    return responses