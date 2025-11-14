from config.config import BASE_URI
from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_401, assert_status_code_404, assert_status_code_400
from src.schemas.customers.customer import CUSTOMER_SCHEMA, CUSTOMER_SCHEMA_IND, CUSTOMER_POST_RESPONSE_SCHEMA, CUSTOMER_PAYLOAD_SCHEMA, CUSTOMER_EDIT_PAYLOAD_SCHEMA
from src.bagisto_api.api_request import BagistoRequest
from src.assertions.customer.response_assertions import assert_valid_schema, assert_response_contiene_data_y_meta, assert_response_contiene_campo
from src.bagisto_api.endpoint import Endpoint
from src.helpers.customer_helper import CustomerHelper
import requests
import pytest
from src.utils.auth import get_auth_headers
import time

@pytest.mark.positivas
@pytest.mark.humo
@pytest.mark.eliminar_cliente
def test_eliminar_cliente_id_existente_return_200(get_token):
    response_create = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(response_create)
    cliente_id = response_create.json()["data"]["id"]

    url = f"{Endpoint.BASE_CUSTOMER.value}/{cliente_id}"
    time.sleep(1)  
    response = BagistoRequest.delete(url, headers=get_auth_headers(get_token))
    assert_status_code_200(response)
    json_response = response.json()
    assert_response_contiene_campo(json_response, "message")
    assert json_response["message"] == "Customer successfully deleted"

@pytest.mark.negativas
@pytest.mark.regresion
@pytest.mark.eliminar_cliente
def test_eliminar_cliente_id_no_existente_return_404(get_token):
    id_inexistente = 999999
    url = f"{Endpoint.BASE_CUSTOMER.value}/{id_inexistente}"
    response = BagistoRequest.delete(url, headers=get_auth_headers(get_token))
    assert_status_code_404(response)

@pytest.mark.negativas
@pytest.mark.humo
@pytest.mark.eliminar_cliente
def test_eliminar_cliente_dos_veces_return_404(get_token):
    response_create = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(response_create)
    cliente_id = response_create.json()["data"]["id"]

    url = f"{Endpoint.BASE_CUSTOMER.value}/{cliente_id}"
    time.sleep(1)  
    primer_delete = BagistoRequest.delete(url, headers=get_auth_headers(get_token))
    assert_status_code_200(primer_delete)

    segundo_delete = BagistoRequest.delete(url, headers=get_auth_headers(get_token))
    assert_status_code_404(segundo_delete)

@pytest.mark.eliminar_cliente
@pytest.mark.negativas
@pytest.mark.humo
def test_eliminar_cliente_con_token_expirado_return_401(get_token):
    url = Endpoint.BASE_CUSTOMER.value
    response = BagistoRequest.get(url, headers=get_auth_headers("20|65468485548484488481"))
    assert_status_code_401(response)
