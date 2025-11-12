from config.config import BASE_URI
from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_401, assert_status_code_404, assert_status_code_400
from src.schemas.customers.customer import CUSTOMER_SCHEMA, CUSTOMER_SCHEMA_IND, CUSTOMER_POST_RESPONSE_SCHEMA, CUSTOMER_PAYLOAD_SCHEMA, CUSTOMER_EDIT_PAYLOAD_SCHEMA
from src.bagisto_api.api_request import BagistoRequest
from src.assertions.customer.response_assertions import assert_valid_schema, assert_response_contiene_data_y_meta, assert_content_type_es_json, assert_data_es_una_lista, assert_response_total_en_meta, assert_response_contiene_meta, assert_current_page_actual_es_1_por_defecto, assert_current_page_es, assert_response_contiene_campo, assert_content_type_es_json, assert_created_at_en_response, assert_updated_at_en_response, assert_data_no_es_nulo
from src.bagisto_api.endpoint import Endpoint
from src.helpers.customer_helper import CustomerHelper
import requests
import pytest
from src.utils.auth import get_auth_headers
import time

@pytest.mark.actualizar_cliente
def test_actualizar_usuario_con_todos_los_campos_validos_return_200(get_token, customer_teardown):
    response_create = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(response_create)
    cliente_id = response_create.json()["data"]["id"]
    customer_teardown.append(cliente_id)

    update_data = CustomerHelper.create_customer_data(first_name="Bianca", last_name="Fernandez", email=None, gender=None, customer_group_id=1)

    url = f"{Endpoint.BASE_CUSTOMER.value}/{cliente_id}"
    response = BagistoRequest.put(url, headers=get_auth_headers(get_token), json=update_data)
    assert_status_code_200(response)
    json_response = response.json()
    assert_response_contiene_campo(json_response, "message")
    assert_response_contiene_campo(json_response, "data")
    assert json_response["data"]["id"] == cliente_id
    assert json_response["data"]["first_name"] == update_data["first_name"]
    assert json_response["data"]["last_name"] == update_data["last_name"]
    assert json_response["data"]["email"] == update_data["email"]
    assert_content_type_es_json(response)
    assert_valid_schema(json_response, CUSTOMER_SCHEMA_IND)

@pytest.mark.actualizar_cliente
def test_actualizar_usuario_id_no_existente_return_404(get_token):
    id_inexistente = 999999
    update_data = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=None, gender=None, customer_group_id=1)
    url = f"{Endpoint.BASE_CUSTOMER.value}/{id_inexistente}"
    response = BagistoRequest.put(url, headers=get_auth_headers(get_token), json=update_data)
    assert_status_code_404(response)

@pytest.mark.actualizar_cliente
def test_actualizar_usuario_con_datos_validos_verificar_que_created_up_se_actualice(get_token, customer_teardown):
    response_create = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(response_create)
    cliente_id = response_create.json()["data"]["id"]
    customer_teardown.append(cliente_id)
    updated_at_antes = response_create.json()["data"]["updated_at"]
    time.sleep(2)  # Esperar 2 segundos para asegurar que updated_at cambie
    update_data = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=None, gender=None, customer_group_id=1)
    url = f"{Endpoint.BASE_CUSTOMER.value}/{cliente_id}"
    response = BagistoRequest.put(url, headers=get_auth_headers(get_token), json=update_data)
    assert_status_code_200(response)
    json_response = response.json()
    updated_at_despues = json_response["data"]["updated_at"]
    assert updated_at_antes != updated_at_despues, "El campo updated_at debería actualizarse después de la actualización"
    assert_content_type_es_json(response)

@pytest.mark.actualizar_cliente
def test_actualizar_usuario_con_datos_validos_verificar_que_created_at_no_se_actualice(get_token, customer_teardown):
    response_create = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(response_create)
    cliente_id = response_create.json()["data"]["id"]
    customer_teardown.append(cliente_id)
    created_at_antes = response_create.json()["data"]["created_at"]
    time.sleep(2)  # Esperar 2 segundos para asegurar que created_at no cambie
    update_data = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=None, gender=None, customer_group_id=1)
    url = f"{Endpoint.BASE_CUSTOMER.value}/{cliente_id}"
    response = BagistoRequest.put(url, headers=get_auth_headers(get_token), json=update_data)
    assert_status_code_200(response)
    json_response = response.json()
    created_at_despues = json_response["data"]["created_at"]
    assert created_at_antes == created_at_despues, "El campo created_at no debería cambiar después de la actualización"
    assert_content_type_es_json(response)

@pytest.mark.actualizar_cliente
def test_actualizar_usuario_first_name_invalido_excede_255_return_400(get_token):
    response_create = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(response_create)
    cliente_id = response_create.json()["data"]["id"]
    actualizar_data = CustomerHelper.create_customer_data(first_name="A"*260, last_name=None, email=None, gender=None, customer_group_id=1)
    url = f"{Endpoint.BASE_CUSTOMER.value}/{cliente_id}"
    response = BagistoRequest.put(url, headers=get_auth_headers(get_token), json=actualizar_data)
    assert_valid_schema(response.json(), CUSTOMER_EDIT_PAYLOAD_SCHEMA)
    assert_status_code_400(response)

@pytest.mark.actualizar_cliente
def test_actualizar_usuario_last_name_invalido_excede_255_return_400(get_token):
    response_create = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(response_create)
    cliente_id = response_create.json()["data"]["id"]
    actualizar_data = CustomerHelper.create_customer_data(first_name=None, last_name="L"*256, email=None, gender=None, customer_group_id=1)
    url = f"{Endpoint.BASE_CUSTOMER.value}/{cliente_id}"
    response = BagistoRequest.put(url, headers=get_auth_headers(get_token), json=actualizar_data)
    assert_valid_schema(response.json(), CUSTOMER_EDIT_PAYLOAD_SCHEMA)
    assert_status_code_400(response)

@pytest.mark.actualizar_cliente
def test_actualizar_usuario_grupo_inexistente_return_404(get_token):
    response_create = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(response_create)
    cliente_id = response_create.json()["data"]["id"]

    actualizar_data = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=None, gender=None, customer_group_id=9999)
    url = f"{Endpoint.BASE_CUSTOMER.value}/{cliente_id}"
    response = BagistoRequest.put(url, headers=get_auth_headers(get_token), json=actualizar_data)
    assert_status_code_404(response)

@pytest.mark.actualizar_cliente
def test_actualizar_usuario_email_duplicado_return_400(get_token):
    cliente1 = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(cliente1)
    email_cliente1 = cliente1.json()["data"]["email"]

    cliente2 = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(cliente2)
    id_cliente2 = cliente2.json()["data"]["id"]

    update_data = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=email_cliente1, gender=None, customer_group_id=1)
    url = f"{Endpoint.BASE_CUSTOMER.value}/{id_cliente2}"
    response = BagistoRequest.put(url, headers=get_auth_headers(get_token), json=update_data)
    assert_status_code_400(response)