import os
import requests
import pytest
from config.config import BASE_URI
from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_401, assert_status_code_404, assert_status_code_400
import json
import jsonschema
from src.schemas.customers.customer import CUSTOMER_SCHEMA, CUSTOMER_SCHEMA_IND
from src.bagisto_api.api_request import BagistoRequest
from src.assertions.customer.response_assertions import assert_valid_schema, assert_response_contiene_data_y_meta
from src.bagisto_api.endpoint import Endpoint
from src.helpers.customer_helper import CustomerHelper

# Validar que el endpoint devuelve correctamente el detalle de un cliente existente por su ID
@pytest.mark.positivas
@pytest.mark.humo
def test_consultar_cliente_por_id_return_200(get_token):
    response_create = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(response_create)
    cliente_id = response_create.json()["data"]["id"]
    url = f"{Endpoint.BASE_CUSTOMER.value}/{cliente_id}"
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    response = BagistoRequest.get(url, headers=headers)
    json_response = response.json()
    assert_status_code_200(response)
    assert response.headers["Content-Type"] == "application/json", f"Se esperaba 'application/json' pero se obtuvo '{response.headers['Content-Type']}'"
    assert "data" in json_response, "No se encontró el campo 'data'"
    assert json_response["data"]["id"] == cliente_id, f"El ID del cliente no coincide con el solicitado ({cliente_id})"
    assert_valid_schema(json_response, CUSTOMER_SCHEMA_IND)


# consultar un cliente con un ID que no existe
@pytest.mark.negativas
@pytest.mark.humo
def test_consultar_cliente_con_id_inexistente_return_404(get_token):
    id_inexistente = 999999
    url = f"{Endpoint.BASE_CUSTOMER.value}/{id_inexistente}"
    headers = {"Authorization": f"Bearer {get_token}"}
    response = BagistoRequest.get(url, headers=headers)
    assert_status_code_404(response)

#consultar un cliente con un ID invalido (no numerico)
@pytest.mark.negativas
@pytest.mark.regresion
def test_consultar_cliente_con_id_no_entero_return_400(get_token):
    id_invalido = "abc#"
    url = f"{Endpoint.BASE_CUSTOMER.value}/{id_invalido}"
    headers = {"Authorization": f"Bearer {get_token}"}
    response = BagistoRequest.get(url, headers=headers)
    assert_status_code_400(response)

#consultar un cliente con un ID negativo
@pytest.mark.negativas
@pytest.mark.regresion
def test_consultar_cliente_con_id_negativos_return_404(get_token):
    id_invalido = -10
    url = f"{Endpoint.BASE_CUSTOMER.value}/{id_invalido}"
    headers = {"Authorization": f"Bearer {get_token}"}
    response = BagistoRequest.get(url, headers=headers)
    assert_status_code_404(response)

#intentar consultar un cliente sin token de autenticacion
@pytest.mark.negativas
@pytest.mark.humo
def test_consultar_cliente_sin_token_return_401(get_token):
    response_create = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(response_create)
    cliente_id = response_create.json()["data"]["id"]
    url = f"{Endpoint.BASE_CUSTOMER.value}/{cliente_id}"
    response = BagistoRequest.get(url)
    assert_status_code_401(response)

#intentar consultar un cliente con token expirado
@pytest.mark.negativas
@pytest.mark.humo
def test_consultar_cliente_con_token_expirado_return_401(get_token):
    response_create = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(response_create)
    cliente_id = response_create.json()["data"]["id"]
    url = f"{Endpoint.BASE_CUSTOMER.value}/{cliente_id}"
    headers = {
        "Authorization": "Bearer 95|JU9nP77BVdVL5HfpV0UTNP4ZbvZ4VkrLeURmY8pjd44f45b0"
    }
    response = BagistoRequest.get(url, headers=headers)
    assert_status_code_401(response)

#verificar que la respuesta es en formato JSON
@pytest.mark.positivas
@pytest.mark.humo
def test_consultar_cliente_por_id_response_json(get_token):
    response_create = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(response_create)
    cliente_id = response_create.json()["data"]["id"]
    url = f"{Endpoint.BASE_CUSTOMER.value}/{cliente_id}"
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    response = BagistoRequest.get(url, headers=headers)
    assert_status_code_200(response)
    assert response.headers["Content-Type"] == "application/json", f"Se esperaba 'application/json' pero se obtuvo '{response.headers['Content-Type']}'"
