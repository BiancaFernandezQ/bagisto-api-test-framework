import os
import requests
import pytest
from config.config import BASE_URI
from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_401, assert_status_code_404, assert_status_code_400
import json
import jsonschema
import time
from src.schemas.groups.groups_schemas import GROUPS_SCHEMA_BODY, GROUP_SCHEMA_IND, CREATE_BODY_GROUP_SCHEMA
from src.bagisto_api.api_request import BagistoRequest
from src.assertions.customer.response_assertions import assert_valid_schema, assert_response_contiene_data_y_meta
from src.bagisto_api.endpoint import Endpoint
from src.helpers.groups_helper import GroupHelper

def test_crear_grupo_con_ambos_campos_validos_return_200(get_token):
    grupo = GroupHelper.create_grupo_data(name=None, code=None)
    url = Endpoint.BASE_GROUP.value
    headers = {
        "Authorization": f"Bearer {get_token}",
        "Content-Type": "application/json"
    }
    response = BagistoRequest.post(url, headers=headers, json=grupo)
    json_response = response.json()
    assert_status_code_200(response)
    assert response.headers["Content-Type"] == "application/json"
    assert "data" in json_response, "No se encontró el campo 'data'"
    assert "message" in json_response, "No se encontró el campo 'message'"
    assert_valid_schema(json_response, CREATE_BODY_GROUP_SCHEMA)
    assert json_response["data"]["name"] == grupo["name"], f"El nombre del grupo no coincide con el enviado ({grupo['name']})"

def test_verificar_created_at_y_updated_at_se_generen_return_200(get_token):
    grupo = GroupHelper.create_grupo_data(name=None, code=None)
    url = Endpoint.BASE_GROUP.value
    headers = {
        "Authorization": f"Bearer {get_token}",
        "Content-Type": "application/json"
    }
    response = BagistoRequest.post(url, headers=headers, json=grupo)
    json_response = response.json()
    assert_status_code_200(response)
    assert_valid_schema(json_response, CREATE_BODY_GROUP_SCHEMA)
    assert json_response["data"]["created_at"] is not None, "El campo 'created_at' es None"
    assert json_response["data"]["updated_at"] is not None, "El campo 'updated_at' es None"

def test_verificar_id_se_genere_automaticamente_return_200(get_token):
    grupo = GroupHelper.create_grupo_data(name=None, code=None)
    url = Endpoint.BASE_GROUP.value
    headers = {
        "Authorization": f"Bearer {get_token}",
        "Content-Type": "application/json"
    }
    response = BagistoRequest.post(url, headers=headers, json=grupo)
    assert_status_code_200(response)
    json_response = response.json()
    assert_valid_schema(json_response, CREATE_BODY_GROUP_SCHEMA)
    assert json_response["data"]["id"] is not None, "El campo 'id' es None"

def test_crear_grupo_solo_con_campo_name_return_400(get_token):
    grupo = GroupHelper.create_grupo_data(name=None, code=None)
    grupo.pop("code", None) # Eliminar el campo 'code' para simular la ausencia

    url = Endpoint.BASE_GROUP.value
    headers = {
        "Authorization": f"Bearer {get_token}",
        "Content-Type": "application/json"
    }

    response = BagistoRequest.post(url, headers=headers, json=grupo)
    assert_status_code_400(response)

def test_crear_grupo_solo_con_campo_code_return_400(get_token):
    grupo = GroupHelper.create_grupo_data(name=None, code=None)
    grupo.pop("name", None) # Eliminar el campo 'name' para simular la ausencia

    url = Endpoint.BASE_GROUP.value
    headers = {
        "Authorization": f"Bearer {get_token}",
        "Content-Type": "application/json"
    }

    response = BagistoRequest.post(url, headers=headers, json=grupo)
    assert_status_code_400(response)

def test_crear_grupo_con_code_conteniendo_espacios_return_400(get_token):
    grupo = GroupHelper.create_grupo_data(name=f"Grupo con Espacios{int(time.time())}", code=f"code con spaces{int(time.time())}")

    url = Endpoint.BASE_GROUP.value
    headers = {
        "Authorization": f"Bearer {get_token}",
        "Content-Type": "application/json"
    }
    
    response = BagistoRequest.post(url, headers=headers, json=grupo)    
    assert_status_code_400(response)

def test_crear_grupo_con_code_conteniendo_guion_bajo_return_400(get_token):
    grupo = GroupHelper.create_grupo_data(name=f"Grupo Underscore{int(time.time())}", code=f"code_con_underscore{int(time.time())}")
    url = Endpoint.BASE_GROUP.value
    headers = {
        "Authorization": f"Bearer {get_token}",
        "Content-Type": "application/json"
    }
    
    response = BagistoRequest.post(url, headers=headers, json=grupo)    
    assert_status_code_400(response)

def test_crear_grupo_con_code_duplicado_no_unico_return_400(get_token):
    grupo_original = GroupHelper.create_grupo_data(name=None, code=None)
    headers_primero = {
        "Authorization": f"Bearer {get_token}",
        "Content-Type": "application/json"
    }
    primer_grupo = BagistoRequest.post(Endpoint.BASE_GROUP.value, headers=headers_primero, json=grupo_original)
    assert_status_code_200(primer_grupo), "No se pudo crear el primer grupo"

    #crear grupo con mismo code y diferente name
    grupo_duplicado = GroupHelper.create_grupo_data(name=f"Grupo Duplicado {int(time.time())}", code=grupo_original["code"])
    headers_segundo = {
        "Authorization": f"Bearer {get_token}",
        "Content-Type": "application/json"
    }
    segundo_grupo = BagistoRequest.post(Endpoint.BASE_GROUP.value, headers=headers_segundo, json=grupo_duplicado)
    assert_status_code_400(segundo_grupo), "Se esperaba un error 400 al crear un grupo con código duplicado"

def test_verificar_id_se_autogenera_al_crear_grupo_return_200(get_token):
    grupo = GroupHelper.create_grupo_data(name=None, code=None)
    url = Endpoint.BASE_GROUP.value
    headers = {
        "Authorization": f"Bearer {get_token}",
        "Content-Type": "application/json"
    }
    response = BagistoRequest.post(url, headers=headers, json=grupo)
    json_response = response.json()
    assert_status_code_200(response)
    assert_valid_schema(json_response, CREATE_BODY_GROUP_SCHEMA)
    assert json_response["data"]["id"] is not None, "El campo 'id' no se generó automáticamente"

@pytest.mark.prueba
def test_verificar_name_acepta_numeros_return_200(get_token):
    grupo = GroupHelper.create_grupo_data(name=int(time.time()), code=None)
    url = Endpoint.BASE_GROUP.value
    headers ={
        "Authorization": f"Bearer {get_token}",
        "Content-Type": "application/json"
    }

    response = BagistoRequest.post(url, headers=headers, json=grupo)
    json_response = response.json()
    assert_status_code_200(response)
    assert_valid_schema(json_response, CREATE_BODY_GROUP_SCHEMA)
    assert json_response["data"]["name"] == grupo["name"]

