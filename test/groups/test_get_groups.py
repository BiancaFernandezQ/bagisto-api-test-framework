from config.config import BASE_URI
from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_401, assert_status_code_404, assert_status_code_400
from src.schemas.groups.groups_schemas import GROUPS_SCHEMA_BODY
from src.bagisto_api.api_request import BagistoRequest
from src.assertions.customer.response_assertions import assert_valid_schema, assert_response_contiene_data_y_meta
from src.bagisto_api.endpoint import Endpoint
from src.helpers.groups_helper import GroupHelper
import requests
import pytest
import time

def test_autenticado_obtener_grupos_return_200(get_token, create_5_groups):
    url = Endpoint.BASE_GROUP.value
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    response = BagistoRequest.get(url, headers=headers)
    
    assert_status_code_200(response)
    json_response = response.json()
    assert_response_contiene_data_y_meta(json_response)
    assert len(json_response["data"]) 
    print("Respuesta JSON completa:", json_response)
    assert_valid_schema(json_response, GROUPS_SCHEMA_BODY)

def test_obtener_todos_grupos_si_paginacion_es_0(get_token, create_5_groups):
    url = Endpoint.BASE_GROUP.value
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    params = {
        "page": 0
    }
    response = BagistoRequest.get(url, headers=headers, params=params)
    assert_status_code_200(response)
    json_response = response.json()
    assert_valid_schema(json_response, GROUPS_SCHEMA_BODY)
    assert_response_contiene_data_y_meta(json_response)
    assert len(json_response.get("data", [])) > 0
    assert response.json()["meta"]["current_page"] == 0 

def test_obtener_grupos








    
