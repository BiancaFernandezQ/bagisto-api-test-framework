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
from src.assertions.customer.response_assertions import assert_valid_schema, assert_response_contiene_data_y_meta
from src.bagisto_api.endpoint import Endpoint
from src.helpers.groups_helper import GroupHelper

def test_eliminar_grupo_valido_id_existente_return_200(get_token):
    response_create = GroupHelper.create_random_group(get_token)
    assert_status_code_200(response_create)
    grupo_id = response_create.json()["data"]["id"]

    url = f"{Endpoint.BASE_GROUP.value}/{grupo_id}"
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    time.sleep(2)  
    response = BagistoRequest.delete(url, headers=headers)
    assert_status_code_200(response)
    json_response = response.json()
    assert "message" in json_response, "No se encontró el campo 'message' en la respuesta"
    assert json_response["message"] == "Customer group successfully deleted"

def test_eliminar_grupo_id_no_existente_return_404(get_token):
    id_inexistente = 999999
    url = f"{Endpoint.BASE_GROUP.value}/{id_inexistente}"
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    response = BagistoRequest.delete(url, headers=headers)
    assert_status_code_404(response)

def test_eliminar_grupo_con_token_expirado_return_401(get_token):
    url = Endpoint.BASE_GROUP.value
    headers = {"Authorization": "Bearer 206546848554848448481"}
    response = BagistoRequest.get(url, headers=headers)
    assert_status_code_401(response)

def test_eliminar_grupo_valido_dos_veces_return_404(get_token):
    response_create = GroupHelper.create_random_group(get_token)
    assert_status_code_200(response_create)
    grupo_id = response_create.json()["data"]["id"]

    url = f"{Endpoint.BASE_GROUP.value}/{grupo_id}"
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    time.sleep(1)  
    primer_delete = BagistoRequest.delete(url, headers=headers)
    assert_status_code_200(primer_delete)

    segundo_delete = BagistoRequest.delete(url, headers=headers)
    assert_status_code_404(segundo_delete)
