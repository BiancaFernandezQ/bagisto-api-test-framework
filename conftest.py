import pytest
import requests
from config.config import ADMIN_EMAIL, ADMIN_PASSWORD, DEVICE_NAME
from src.bagisto_api.endpoint import Endpoint
from src.helpers.customer_helper import CustomerHelper
from src.helpers.groups_helper import GroupHelper
from src.bagisto_api.api_request import BagistoRequest
from src.utils.auth import get_auth_headers
import src.utils.logger as logger

log = logger.setup_logger("conftest")

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
    log.info(response.status_code)
    token = response.json().get("token")
    log.debug(f"Token obtenido: {token}")
    assert token, "No se recibió token en la respuesta"
    return token

@pytest.fixture(scope="session")
def create_15_customers(get_token):
    log.info("Iniciando creación de 15 clientes para las pruebas")
    responses = CustomerHelper.create_multiple_random_customers(get_token, 15)
    created_ids = []
    for i, response in enumerate(responses):
        assert response.status_code == 200, f"Fallo al crear el cliente #{i+1}. Status: {response.status_code}, Body: {response.text}"
        created_ids.append(response.json()["data"]["id"])
    
    yield responses 

    log.info("Iniciando teardown: Eliminando los 15 clientes de prueba")
    for customer_id in created_ids:
        url = f"{Endpoint.BASE_CUSTOMER.value}/{customer_id}"
        BagistoRequest.delete(url, headers=get_auth_headers(get_token))
    log.info("Teardown completado: Clientes eliminados")

@pytest.fixture(scope="function")
def create_customer(get_token):
    log.info("Creando cliente para la prueba")
    response_create = CustomerHelper.create_random_customer(get_token)
    assert response_create.status_code == 200, f"SETUP FAILED: No se pudo crear el cliente. Body: {response_create.text}"
    customer_data = response_create.json()
    customer_id = customer_data["data"]["id"]
    log.info(f"Cliente creado con ID: {customer_id}")

    yield customer_data  

    log.info(f"Iniciando teardown: Eliminando el cliente con ID: {customer_id}")
    url = f"{Endpoint.BASE_CUSTOMER.value}/{customer_id}"
    BagistoRequest.delete(url, headers=get_auth_headers(get_token))
    log.info("Teardown completado: Cliente eliminado")

@pytest.fixture(scope="function")
def customer_teardown(get_token):
    customer_ids_to_delete = []
    yield customer_ids_to_delete

    log.info("Iniciando teardown: Eliminando clientes creados durante la prueba")
    for customer_id in customer_ids_to_delete:
        log.info(f"Eliminando cliente con ID: {customer_id}")
        CustomerHelper.delete_customer(get_token, customer_id)
    log.info("Teardown completado: Clientes eliminados")


@pytest.fixture(scope="session")
def create_5_groups(get_token):
    log.info("Iniciando creación de 5 grupos para las pruebas")
    responses = GroupHelper.create_multiple_random_groups(get_token, 5)
    created_ids = []
    for i, response in enumerate(responses):
        assert response.status_code == 200, f"Fallo al crear el grupo #{i+1}. Status: {response.status_code}, Body: {response.text}"
        created_ids.append(response.json()["data"]["id"])
    
    yield responses

    log.info("Iniciando teardown: Eliminando los 5 grupos de prueba")
    for group_id in created_ids:
        url = f"{Endpoint.BASE_GROUP.value}/{group_id}"
        BagistoRequest.delete(url, headers=get_auth_headers(get_token))
    log.info("Teardown completado: Grupos eliminados")

@pytest.fixture(scope="function")
def create_group(get_token):
    log.info("Creando grupo para la prueba")
    response_create = GroupHelper.create_random_group(get_token)
    assert response_create.status_code == 200, f"SETUP FAILED: No se pudo crear el grupo. Body: {response_create.text}"
    group_data = response_create.json()
    group_id = group_data["data"]["id"]
    log.info(f"Grupo creado con ID: {group_id}")

    yield group_data

    log.info(f"Iniciando teardown: Eliminando el grupo con ID: {group_id}")
    url = f"{Endpoint.BASE_GROUP.value}/{group_id}"
    BagistoRequest.delete(url, headers=get_auth_headers(get_token))
    log.info("Teardown completado: Grupo eliminado")

@pytest.fixture(scope="function")
def group_teardown(get_token):
    group_ids_to_delete = []
    yield group_ids_to_delete

    log.info("Iniciando teardown: Eliminando grupos creados durante la prueba")
    for group_id in group_ids_to_delete:
        log.info(f"Eliminando grupo con ID: {group_id}")
        GroupHelper.delete_group(get_token, group_id)
    log.info("Teardown completado: Grupos eliminados")