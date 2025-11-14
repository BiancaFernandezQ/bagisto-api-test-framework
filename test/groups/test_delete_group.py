import os
import requests
import pytest
from config.config import BASE_URI
from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_401, assert_status_code_404, assert_status_code_400
import json
import jsonschema
import time
from src.schemas.groups.groups_schemas import GROUPS_SCHEMA_BODY, GROUP_SCHEMA_IND, CREATE_BODY_GROUP_SCHEMA, GROUPS_PAYLOAD_SCHEMA
from src.bagisto_api.api_request import BagistoRequest
from src.assertions.customer.response_assertions import assert_valid_schema, assert_response_contiene_data_y_meta, assert_response_contiene_campo, assert_content_type_es_json
from src.bagisto_api.endpoint import Endpoint
from src.helpers.groups_helper import GroupHelper
from src.helpers.customer_helper import CustomerHelper
from src.utils.auth import get_auth_headers

@pytest.mark.positivas
@pytest.mark.humo
@pytest.mark.eliminar_grupo
def test_eliminar_grupo_valido_id_existente_return_200(get_token):
    response_create = GroupHelper.create_random_group(get_token)
    assert_status_code_200(response_create)
    grupo_id = response_create.json()["data"]["id"]

    url = f"{Endpoint.BASE_GROUP.value}/{grupo_id}"
    time.sleep(2)  
    response = BagistoRequest.delete(url, headers=get_auth_headers(get_token))
    assert_status_code_200(response)
    json_response = response.json()
    assert_response_contiene_campo(json_response, "message")
    assert_content_type_es_json(response)
    assert json_response["message"] == "Customer group successfully deleted"

@pytest.mark.negativas
@pytest.mark.regresion
@pytest.mark.eliminar_grupo
def test_eliminar_grupo_id_no_existente_return_404(get_token):
    id_inexistente = 999999
    url = f"{Endpoint.BASE_GROUP.value}/{id_inexistente}"
    response = BagistoRequest.delete(url, headers=get_auth_headers(get_token))
    assert_status_code_404(response)

@pytest.mark.negativas
@pytest.mark.humo
@pytest.mark.eliminar_grupo
def test_eliminar_grupo_con_token_expirado_return_401():
    url = Endpoint.BASE_GROUP.value
    response = BagistoRequest.get(url, headers=get_auth_headers("20|65468485548484488481"))
    assert_status_code_401(response)

@pytest.mark.negativas
@pytest.mark.humo
@pytest.mark.eliminar_grupo
def test_eliminar_grupo_valido_dos_veces_return_404(get_token):
    response_create = GroupHelper.create_random_group(get_token)
    assert_status_code_200(response_create)
    grupo_id = response_create.json()["data"]["id"]

    url = f"{Endpoint.BASE_GROUP.value}/{grupo_id}"
    time.sleep(1)  
    primer_delete = BagistoRequest.delete(url, headers=get_auth_headers(get_token))
    assert_status_code_200(primer_delete)

    segundo_delete = BagistoRequest.delete(url, headers=get_auth_headers(get_token))
    assert_status_code_404(segundo_delete)

@pytest.mark.negativas
@pytest.mark.humo
@pytest.mark.eliminar_grupo
def test_eliminar_grupo_con_clientes_asociados_return_400(get_token):
    response_create = GroupHelper.create_random_group(get_token)
    assert_status_code_200(response_create)
    grupo_id = response_create.json()["data"]["id"]
    
    customer_payload = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=None, gender=None, customer_group_id=grupo_id)
    
    url_customer = Endpoint.BASE_CUSTOMER.value
    response_customer = BagistoRequest.post(url_customer, headers=get_auth_headers(get_token), json=customer_payload)
    time.sleep(1)
    assert_status_code_200(response_customer)

    url_group = f"{Endpoint.BASE_GROUP.value}/{grupo_id}"
    time.sleep(1)  
    response_delete = BagistoRequest.delete(url_group, headers=get_auth_headers(get_token))
    assert_status_code_400(response_delete)