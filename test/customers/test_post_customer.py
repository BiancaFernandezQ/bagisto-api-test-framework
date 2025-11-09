from config.config import BASE_URI
from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_401, assert_status_code_404, assert_status_code_400
from src.schemas.customers.customer import CUSTOMER_SCHEMA, CUSTOMER_SCHEMA_IND, CUSTOMER_POST_RESPONSE_SCHEMA, CUSTOMER_PAYLOAD_SCHEMA
from src.bagisto_api.api_request import BagistoRequest
from src.assertions.customer.response_assertions import assert_valid_schema, assert_response_contiene_data_y_meta, assert_content_type_es_json, assert_data_es_una_lista, assert_response_total_en_meta, assert_response_contiene_meta, assert_current_page_actual_es_1_por_defecto, assert_current_page_es, assert_response_contiene_campo, assert_content_type_es_json, assert_created_at_en_response, assert_updated_at_en_response, assert_data_no_es_nulo
from src.bagisto_api.endpoint import Endpoint
from src.helpers.customer_helper import CustomerHelper
import requests
from src.utils.auth import get_auth_headers
import pytest

def test_crear_cliente_con_todos_los_campos_obligatorios_return_200(get_token, customer_teardown):
    # Datos del cliente a crear
    url = Endpoint.BASE_CUSTOMER.value
    payload = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=None, gender=None, customer_group_id=1)
    response = BagistoRequest.post(url, json=payload, headers=get_auth_headers(get_token))
    json_response = response.json()
    assert_status_code_200(response)
    assert_valid_schema(json_response, CUSTOMER_POST_RESPONSE_SCHEMA)
    assert_response_contiene_campo(json_response, "data")
    assert_response_contiene_campo(json_response, "message")

    customer_teardown.append(json_response["data"]["id"])

    assert_data_no_es_nulo(json_response)
    assert json_response["data"]["id"] is not None
    assert json_response["data"]["first_name"] == payload["first_name"]
    assert json_response["data"]["last_name"] == payload["last_name"]
    assert json_response["data"]["email"] == payload["email"]
    assert json_response["data"]["gender"] == payload["gender"]
    assert json_response["data"]["name"] == payload["first_name"] + " " + payload["last_name"]
    assert_created_at_en_response(json_response)
    assert_updated_at_en_response(json_response)
    assert_content_type_es_json(response)
    assert_valid_schema(payload, CUSTOMER_PAYLOAD_SCHEMA)

def test_crear_cliente_con_todos_los_campos_return_200(get_token, customer_teardown):
    # Datos del cliente a crear
    url = Endpoint.BASE_CUSTOMER.value
    payload = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=None, gender=None, date_of_birth="", phone="", customer_group_id=1)
    response = BagistoRequest.post(url, json=payload, headers=get_auth_headers(get_token))
    json_response = response.json()
    assert_status_code_200(response)
    assert_valid_schema(json_response, CUSTOMER_POST_RESPONSE_SCHEMA)
    assert_response_contiene_campo(json_response, "data")
    assert_response_contiene_campo(json_response, "message")

    customer_teardown.append(json_response["data"]["id"])

    assert_data_no_es_nulo(json_response)
    assert json_response["data"]["id"] is not None
    assert json_response["data"]["first_name"] == payload["first_name"]
    assert json_response["data"]["last_name"] == payload["last_name"]
    assert json_response["data"]["email"] == payload["email"]
    assert json_response["data"]["gender"] == payload["gender"]
    assert json_response["data"]["date_of_birth"] == payload["date_of_birth"]
    assert json_response["data"]["phone"] == payload["phone"]
    assert_created_at_en_response(json_response)
    assert_updated_at_en_response(json_response)
    assert_content_type_es_json(response)
    assert_valid_schema(payload, CUSTOMER_PAYLOAD_SCHEMA)

# crear cliente con genero valido Male o Female o Other
@pytest.mark.parametrize("genero_valido", ["Male", "Female", "Other"])
def test_crear_cliente_con_genero_valido_return_200(get_token, genero_valido, customer_teardown):
    url = Endpoint.BASE_CUSTOMER.value
    payload = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=None, gender=genero_valido, customer_group_id=1)
    response = BagistoRequest.post(url, json=payload, headers=get_auth_headers(get_token))
    json_response = response.json()
    assert_status_code_200(response)
    customer_teardown.append(json_response["data"]["id"])
    assert_valid_schema(json_response, CUSTOMER_POST_RESPONSE_SCHEMA)
    assert_response_contiene_campo(json_response, "data")
    assert_response_contiene_campo(json_response, "message")
    assert_data_no_es_nulo(json_response)
    assert json_response["data"]["gender"] == genero_valido
    assert_content_type_es_json(response)
    assert_valid_schema(payload, CUSTOMER_PAYLOAD_SCHEMA)

def test_crear_cliente_first_name_valido_1_caracter_return_200(get_token, customer_teardown):
    url = Endpoint.BASE_CUSTOMER.value
    payload = CustomerHelper.create_customer_data(first_name="A", last_name=None, email=None, gender=None, customer_group_id=1)
    response = BagistoRequest.post(url, json=payload, headers=get_auth_headers(get_token))
    json_response = response.json()
    assert_status_code_200(response)
    customer_teardown.append(json_response["data"]["id"])
    assert_valid_schema(json_response, CUSTOMER_POST_RESPONSE_SCHEMA)
    assert_response_contiene_campo(json_response, "data")
    assert_response_contiene_campo(json_response, "message")
    assert_data_no_es_nulo(json_response)
    assert json_response["data"]["first_name"] == payload["first_name"]
    assert_content_type_es_json(response)
    assert_valid_schema(payload, CUSTOMER_PAYLOAD_SCHEMA)

def test_crear_cliente_first_name_valido_255_caracteres_return_200(get_token, customer_teardown):
    url = Endpoint.BASE_CUSTOMER.value
    payload = CustomerHelper.create_customer_data(first_name="A"*255, last_name=None, email=None, gender=None, customer_group_id=1) 
    response = BagistoRequest.post(url, json=payload, headers=get_auth_headers(get_token))
    json_response = response.json()
    assert_status_code_200(response)
    customer_teardown.append(json_response["data"]["id"])
    assert_valid_schema(json_response, CUSTOMER_POST_RESPONSE_SCHEMA)
    assert_response_contiene_campo(json_response, "data")
    assert_response_contiene_campo(json_response, "message")
    assert_data_no_es_nulo(json_response)
    assert json_response["data"]["first_name"] == payload["first_name"]
    assert_content_type_es_json(response)
    assert_valid_schema(payload, CUSTOMER_PAYLOAD_SCHEMA)

def test_crear_cliente_first_name_excede_255_caracteres_return_400(get_token):
    url = Endpoint.BASE_CUSTOMER.value
    payload = CustomerHelper.create_customer_data(first_name='Bianca Fernandez Hola Sarahi Lola Laura Ana Bianca Bianca Fernandez Hola Sarahi Lola Laura Ana Bianca Caracteres Sarahi Lola Laura Ana Bianca Caracteres en el Campo FirstName Bianca Fernandez en el Campo FirstName Bianca Fernandez Lola Campo Bianca Fernandez', last_name=None, email=None, gender=None, customer_group_id=1)
    response = BagistoRequest.post(url, json=payload, headers=get_auth_headers(get_token))
    json_response = response.json()
    assert_status_code_400(response)

def test_crear_cliente_last_name_valido_1_caracter_return_200(get_token, customer_teardown):
    url = Endpoint.BASE_CUSTOMER.value
    payload = CustomerHelper.create_customer_data(first_name=None, last_name="L", email=None, gender=None, customer_group_id=1)
    response = BagistoRequest.post(url, json=payload, headers=get_auth_headers(get_token))
    json_response = response.json()
    assert_status_code_200(response)

    customer_teardown.append(json_response["data"]["id"])

    assert_valid_schema(json_response, CUSTOMER_POST_RESPONSE_SCHEMA)
    assert_response_contiene_campo(json_response, "data")
    assert_response_contiene_campo(json_response, "message")
    assert_data_no_es_nulo(json_response)
    assert json_response["data"]["last_name"] == payload["last_name"]
    assert_content_type_es_json(response)
    assert_valid_schema(payload, CUSTOMER_PAYLOAD_SCHEMA)

def test_crear_cliente_last_name_valido_255_caracteres_return_200(get_token, customer_teardown):
    url = Endpoint.BASE_CUSTOMER.value
    payload = CustomerHelper.create_customer_data(first_name=None, last_name="L"*255, email=None, gender=None, customer_group_id=1)
    response = BagistoRequest.post(url, json=payload, headers=get_auth_headers(get_token))
    json_response = response.json()
    assert_status_code_200(response)
    customer_teardown.append(json_response["data"]["id"])
    assert_valid_schema(json_response, CUSTOMER_POST_RESPONSE_SCHEMA)
    assert_response_contiene_campo(json_response, "data")
    assert_response_contiene_campo(json_response, "message")
    assert_data_no_es_nulo(json_response)
    assert json_response["data"]["last_name"] == payload["last_name"]
    assert_content_type_es_json(response)
    assert_valid_schema(payload, CUSTOMER_PAYLOAD_SCHEMA)

def test_crear_cliente_last_name_excede_255_caracteres_return_400(get_token):
    url = Endpoint.BASE_CUSTOMER.value
    payload = CustomerHelper.create_customer_data(first_name=None, last_name='Fernandez Quispe Apellido Aqui Hola Mundo Hola Mundo Pytest Aqui Apellidos Apellidos Apellidos Hola Last Name Fernandez Quispe Apellido Aqui Hola Mundo Fernandez Quispe Apellido Aqui Hola MundoFernandez Quispe Apellido Aqui Hola Mundo Fernandez Quispe Apellido', email=None, gender=None, customer_group_id=1)
    response = BagistoRequest.post(url, json=payload, headers=get_auth_headers(get_token))
    json_response = response.json()
    assert_status_code_400(response)

def test_validar_campo_name_se_genera_automaticamente_al_crear_cliente(get_token, customer_teardown):
    url = Endpoint.BASE_CUSTOMER.value
    payload = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=None, gender=None, customer_group_id=1)
    response = BagistoRequest.post(url, json=payload, headers=get_auth_headers(get_token))
    json_response = response.json()
    assert_status_code_200(response)
    customer_teardown.append(json_response["data"]["id"])
    assert_valid_schema(json_response, CUSTOMER_POST_RESPONSE_SCHEMA)
    assert_response_contiene_campo(json_response, "data")
    assert_response_contiene_campo(json_response, "message")
    assert_data_no_es_nulo(json_response)
    assert json_response["data"]["first_name"] == payload["first_name"]
    assert json_response["data"]["last_name"] == payload["last_name"]   
    assert json_response["data"]["name"] == payload["first_name"] + " " + payload["last_name"]
    assert_content_type_es_json(response)
    assert_valid_schema(payload, CUSTOMER_PAYLOAD_SCHEMA)

@pytest.mark.negativas
def test_crear_cliente_email_duplicado_return_400(get_token): 
    url = Endpoint.BASE_CUSTOMER.value
    # Crear un cliente inicial para obtener un email duplicado
    payload_inicial = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=None, gender=None, customer_group_id=1)
    response_inicial = BagistoRequest.post(url, json=payload_inicial, headers=get_auth_headers(get_token))
    assert_status_code_200(response_inicial)

    # Intentar crear otro cliente con el mismo email
    payload_duplicado = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=payload_inicial["email"], gender=None, customer_group_id=1)
    response_duplicado = BagistoRequest.post(url, json=payload_duplicado, headers=get_auth_headers(get_token))
    assert_status_code_400(response_duplicado)

def test_verificar_creacion_cliente_con_email_invalido_return_400(get_token):
    url = Endpoint.BASE_CUSTOMER.value
    payload = CustomerHelper.create_customer_data(first_name=None, last_name=None, email="emailinvalido", gender=None, customer_group_id=1)
    response = BagistoRequest.post(url, json=payload, headers=get_auth_headers(get_token))
    assert_status_code_400(response)

@pytest.mark.negativas
def test_crear_cliente_con_grupo_inexistente_return_404(get_token):
    grupo_invalido_id = 999999
    url = Endpoint.BASE_CUSTOMER.value
    payload = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=None, gender=None, customer_group_id=grupo_invalido_id)
    response = BagistoRequest.post(url, json=payload, headers=get_auth_headers(get_token))
    assert_status_code_404(response)

@pytest.mark.negativas
def test_campos_obligatorios_vacios_return_400(get_token):
    url = Endpoint.BASE_CUSTOMER.value
    payload = {
        "first_name": "",
        "last_name": "",
        "email": "",
        "gender": "",
        "customer_group_id": ""
    }
    response = BagistoRequest.post(url, json=payload, headers=get_auth_headers(get_token))
    assert_status_code_400(response)

def test_crear_clientes_payload_valido_esquema(get_token, customer_teardown):
    url = Endpoint.BASE_CUSTOMER.value
    payload = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=None, gender=None, customer_group_id=1)
    assert_valid_schema(payload, CUSTOMER_PAYLOAD_SCHEMA)
    response = BagistoRequest.post(url, json=payload, headers=get_auth_headers(get_token))
    assert_status_code_200(response)
    customer_teardown.append(response.json()["data"]["id"])

def test_validar_payload_crear_cliente_con_campos_opcionales(get_token, customer_teardown):
    url = Endpoint.BASE_CUSTOMER.value
    payload = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=None, gender=None, date_of_birth=None, phone=None, customer_group_id=1)
    assert_valid_schema(payload, CUSTOMER_PAYLOAD_SCHEMA)
    response = BagistoRequest.post(url, json=payload, headers=get_auth_headers(get_token))
    assert_status_code_200(response)
    customer_teardown.append(response.json()["data"]["id"])