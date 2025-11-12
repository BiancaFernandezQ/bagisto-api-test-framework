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
from src.assertions.customer.response_assertions import assert_valid_schema, assert_response_contiene_data_y_meta, assert_content_type_es_json, assert_response_contiene_campo
from src.bagisto_api.endpoint import Endpoint
from src.helpers.groups_helper import GroupHelper
from src.utils.auth import get_auth_headers

@pytest.mark.actualizar_grupo
def test_actulizar_grupo_existente_valido_return_200(get_token, group_teardown):
    grupo_creado = GroupHelper.create_random_group(get_token)
    assert_status_code_200(grupo_creado)
    grupo_id = grupo_creado.json()["data"]["id"]
    group_teardown.append(grupo_id)
    grupo_datos = GroupHelper.create_grupo_data(name=None, code=None)
    url = f"{Endpoint.BASE_GROUP.value}/{grupo_id}"
    response = BagistoRequest.put(url, headers=get_auth_headers(get_token), json=grupo_datos)
    assert_valid_schema(grupo_datos, GROUPS_PAYLOAD_SCHEMA)
    assert_status_code_200(response)
    json_response = response.json()
    assert_valid_schema(json_response, CREATE_BODY_GROUP_SCHEMA )
    assert_response_contiene_campo(json_response, "message")
    assert_response_contiene_campo(json_response, "data")
    assert json_response["data"]["id"] == grupo_id
    assert json_response["data"]["name"] == grupo_datos["name"]
    assert_content_type_es_json(response)

@pytest.mark.actualizar_grupo
def test_actualizar_grupo_id_no_existente_return_404(get_token):
    id_inexistente = 999999
    grupo_datos = GroupHelper.create_grupo_data(name=None, code=None)
    url = f"{Endpoint.BASE_GROUP.value}/{id_inexistente}"
    response = BagistoRequest.put(url, headers=get_auth_headers(get_token), json=grupo_datos)
    assert_status_code_404(response)

@pytest.mark.actualizar_grupo
def test_verificar_updated_at_se_actualice_al_actualizar_grupo(get_token, group_teardown):
    grupo_creado = GroupHelper.create_random_group(get_token)
    assert_status_code_200(grupo_creado)
    time.sleep(2)

    grupo_id = grupo_creado.json()["data"]["id"]
    group_teardown.append(grupo_id)
    
    updated_at_antes = grupo_creado.json()["data"]["updated_at"]
    grupo_datos = GroupHelper.create_grupo_data(name=None, code=None)
    url = f"{Endpoint.BASE_GROUP.value}/{grupo_id}"
    response = BagistoRequest.put(url, headers=get_auth_headers(get_token), json=grupo_datos)
    assert_status_code_200(response)
    json_response = response.json()
    updated_at_despues = json_response["data"]["updated_at"]
    assert_valid_schema(grupo_datos, GROUPS_PAYLOAD_SCHEMA) #vrificar lo que enviamos
    assert_valid_schema(json_response, CREATE_BODY_GROUP_SCHEMA)  #verificar lo que recibimos
    assert updated_at_antes != updated_at_despues, "El campo updated_at no se actualizó correctamente"
    assert_content_type_es_json(response)

@pytest.mark.actualizar_grupo
def test_verificar_created_at_no_se_actualice_al_actualizar_grupo(get_token, group_teardown):
    grupo_creado = GroupHelper.create_random_group(get_token) #crear grupo primero
    assert_status_code_200(grupo_creado)
    grupo_id = grupo_creado.json()["data"]["id"]
    group_teardown.append(grupo_id)
    created_at_antes = grupo_creado.json()["data"]["created_at"]

    time.sleep(2)
    
    grupo_datos = GroupHelper.create_grupo_data(name=None, code=None)
    url = f"{Endpoint.BASE_GROUP.value}/{grupo_id}"
    response = BagistoRequest.put(url, headers=get_auth_headers(get_token), json=grupo_datos)
    assert_status_code_200(response)
    json_response = response.json()
    created_at_despues = json_response["data"]["created_at"]
    assert_valid_schema(grupo_datos, GROUPS_PAYLOAD_SCHEMA) #vrificar lo que enviamos
    assert_valid_schema(json_response, CREATE_BODY_GROUP_SCHEMA)  #verificar lo que recibimos
    assert created_at_antes == created_at_despues, "El campo created_at se modificó al actualizar el grupo"
    assert_content_type_es_json(response)

@pytest.mark.actualizar_grupo
def test_actualizar_grupo_payload_vacio_return_400(get_token, group_teardown):
    grupo_creado = GroupHelper.create_random_group(get_token)
    assert_status_code_200(grupo_creado)
    grupo_id = grupo_creado.json()["data"]["id"]
    group_teardown.append(grupo_id)
    grupo_datos = {}
    url = f"{Endpoint.BASE_GROUP.value}/{grupo_id}"
    response = BagistoRequest.put(url, headers=get_auth_headers(get_token), json=grupo_datos)
    assert_status_code_400(response)

@pytest.mark.actualizar_grupo
def test_verificar_que_no_se_actualice_grupo_si_falta_name(get_token, group_teardown):
    grupo_creado = GroupHelper.create_random_group(get_token)
    assert_status_code_200(grupo_creado)
    time.sleep(1)
    grupo_id = grupo_creado.json()["data"]["id"]
    group_teardown.append(grupo_id)
    grupo_datos = {
        "code": "NuevoCodigo"+str(int(time.time() * 1000))
    }
    url = f"{Endpoint.BASE_GROUP.value}/{grupo_id}"
    response = BagistoRequest.put(url, headers=get_auth_headers(get_token), json=grupo_datos)
    assert_status_code_400(response)

@pytest.mark.actualizar_grupo
def test_verificar_que_no_se_actualice_grupo_si_falta_code(get_token, group_teardown):
    grupo_creado = GroupHelper.create_random_group(get_token)
    assert_status_code_200(grupo_creado)
    time.sleep(1)

    grupo_id = grupo_creado.json()["data"]["id"]
    group_teardown.append(grupo_id)
    grupo_datos = {
        "name": "NuevoNombre"+str(int(time.time() * 1000))
    }
    url = f"{Endpoint.BASE_GROUP.value}/{grupo_id}"
    response = BagistoRequest.put(url, headers=get_auth_headers(get_token), json=grupo_datos)
    assert_status_code_400(response)