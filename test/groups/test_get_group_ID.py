import os
import requests
import pytest
from config.config import BASE_URI
from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_401, assert_status_code_404, assert_status_code_400
import json
import jsonschema
import time
from src.schemas.groups.groups_schemas import GROUPS_SCHEMA_BODY, GROUP_SCHEMA_IND
from src.bagisto_api.api_request import BagistoRequest
from src.assertions.customer.response_assertions import assert_valid_schema, assert_response_contiene_data_y_meta, assert_content_type_es_json, assert_response_contiene_data
from src.bagisto_api.endpoint import Endpoint
from src.helpers.groups_helper import GroupHelper
from src.utils.auth import get_auth_headers

@pytest.mark.listar_grupo_especifico
@pytest.mark.positivas
@pytest.mark.humo
def test_consultar_grupo_por_id_return_200(get_token, create_group):
    grupo_id = create_group["data"]["id"]
    url = f"{Endpoint.BASE_GROUP.value}/{grupo_id}"
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token))
    json_response = response.json()
    assert_status_code_200(response)
    assert_content_type_es_json(response)
    assert_response_contiene_data(json_response)
    assert json_response["data"]["id"] == grupo_id, f"El ID del grupo no coincide con el solicitado ({grupo_id})"
    assert_valid_schema(json_response, GROUP_SCHEMA_IND)

@pytest.mark.listar_grupo_especifico
@pytest.mark.negativas
@pytest.mark.humo
def test_consultar_grupo_con_id_inexistente_return_404(get_token):
    id_inexistente = 999999
    url = f"{Endpoint.BASE_GROUP.value}/{id_inexistente}"
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token))
    assert_status_code_404(response)

@pytest.mark.listar_grupo_especifico
@pytest.mark.negativas
@pytest.mark.regresion
def test_consultar_grupo_con_id_no_entero_return_400(get_token):
    id_invalido = "abc#"
    url = f"{Endpoint.BASE_GROUP.value}/{id_invalido}"
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token))
    assert_status_code_400(response)

@pytest.mark.listar_grupo_especifico
@pytest.mark.negativas
@pytest.mark.regresion
def test_consultar_grupo_con_id_negativos_return_404(get_token):
    id_invalido = -10
    url = f"{Endpoint.BASE_GROUP.value}/{id_invalido}"
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token))
    assert_status_code_404(response)

@pytest.mark.listar_grupo_especifico
@pytest.mark.negativas
@pytest.mark.humo
def test_consultar_grupo_sin_token_return_401(create_group):
    grupo_id = create_group["data"]["id"]
    url = f"{Endpoint.BASE_GROUP.value}/{grupo_id}"
    response = BagistoRequest.get(url)
    assert_status_code_401(response)

@pytest.mark.listar_grupo_especifico
@pytest.mark.negativas
@pytest.mark.humo
def test_consultar_grupo_con_token_expirado_return_401(create_group):
    grupo_id = create_group["data"]["id"]
    url = f"{Endpoint.BASE_GROUP.value}/{grupo_id}"
    response = BagistoRequest.get(url, headers=get_auth_headers("95|JU9nP77BVdVL5HfpV0UTNP4ZbvZ4VkrLeURmY8pjd"))
    assert_status_code_401(response)

@pytest.mark.listar_grupo_especifico
@pytest.mark.positivas
@pytest.mark.humo
def test_consultar_grupo_por_id_response_json(get_token, create_group):
    grupo_id = create_group["data"]["id"]
    url = f"{Endpoint.BASE_GROUP.value}/{grupo_id}"
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token))
    assert_status_code_200(response)
    assert_content_type_es_json(response)