from config.config import BASE_URI
from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_401, assert_status_code_404, assert_status_code_400
from src.schemas.groups.groups_schemas import GROUPS_SCHEMA_BODY, GROUPS_BODY_PAGINATION_0
from src.bagisto_api.api_request import BagistoRequest
from src.assertions.customer.response_assertions import assert_valid_schema, assert_response_contiene_data_y_meta, assert_response_contiene_data
from src.bagisto_api.endpoint import Endpoint
from src.helpers.groups_helper import GroupHelper
from src.utils.auth import get_auth_headers
import requests
import pytest
import time

def test_autenticado_obtener_grupos_return_200(get_token, create_5_groups):
    url = Endpoint.BASE_GROUP.value
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token))
    
    assert_status_code_200(response)
    json_response = response.json()
    assert_response_contiene_data_y_meta(json_response)
    assert len(json_response["data"]) 
    assert_valid_schema(json_response, GROUPS_SCHEMA_BODY)

def test_obtener_todos_grupos_si_pagination_es_0(get_token, create_5_groups):
    url = Endpoint.BASE_GROUP.value
    response_total = BagistoRequest.get(url, headers=get_auth_headers(get_token))
    assert_status_code_200(response_total)
    total_grupos = response_total.json()["meta"]["total"]
    params = {
        "pagination": 0
    }
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token), params=params)
    assert_status_code_200(response)
    json_response = response.json()
    assert_response_contiene_data(json_response)
    assert len(json_response.get("data", [])) == total_grupos, f"Se esperaba {total_grupos} grupos, pero se obtuvieron {len(json_response.get('data', []))}."
    assert_valid_schema(json_response, GROUPS_BODY_PAGINATION_0)

def test_solicitar_page_inexistente_return_data_vacia(get_token, create_5_groups):
    url = Endpoint.BASE_GROUP.value
    params = {
        "limit": 10,
        "page": 99999  
    }
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token), params=params)
    assert_status_code_200(response)
    json_response = response.json()
    assert len(json_response.get("data", [])) == 0, "Se esperaba una lista vacía de grupos para una página inexistente"

@pytest.mark.parametrize("sort, order", [
    ("id", "asc"),
    ("id", "desc"),
])
def test_consultar_grupos_ordenados(get_token,create_5_groups, sort, order):
    url = f"{Endpoint.BASE_GROUP.value}?sort={sort}&order={order}"
    
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token))
    assert_status_code_200(response)
    
    grupos = response.json()["data"]
    assert grupos == sorted(grupos, key=lambda x: x["id"], reverse=(order == "desc"))

@pytest.mark.negativas
@pytest.mark.humo
def test_solicitar_order_invalido_return_400(get_token, create_5_groups):
    url = f"{Endpoint.BASE_GROUP.value}?sort=id&order=invalid_order"
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token))
    assert_status_code_400(response)

def test_solicitar_sort_campo_inexistente_return_400(get_token, create_5_groups):
    url = f"{Endpoint.BASE_GROUP.value}?sort=no_valido&order=asc"
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token))
    assert_status_code_400(response)

def test_obtener_grupos_limite_valido(get_token, create_5_groups):
    url = Endpoint.BASE_GROUP.value
    params = {
        "limit": 3
    }
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token), params=params)
    assert_status_code_200(response)
    json_response = response.json()
    assert_response_contiene_data(json_response)
    assert len(json_response.get("data", [])) == params["limit"], f"El tamaño de la lista de grupos ({len(json_response.get('data', []))}) no coincide con el limit ({params['limit']})"
    assert response.json()["meta"]["per_page"] == params["limit"], f"El campo 'meta.per_page' ({response.json()['meta']['per_page']}) no coincide con el limit ({params['limit']})"
    assert_valid_schema(json_response, GROUPS_SCHEMA_BODY)

def test_solicitar_limit_cero_return_400(get_token):
    url = Endpoint.BASE_GROUP.value
    params = {
        "limit": 0
    }
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token), params=params)
    assert_status_code_400(response)

@pytest.mark.negativas
@pytest.mark.humo
def test_solicitar_limit_negativo_return_400(get_token):
    url = Endpoint.BASE_GROUP.value
    params = { "limit": -5 }
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token), params=params)
    assert_status_code_400(response)

@pytest.mark.positivas
@pytest.mark.humo
def test_solicitar_limit_minimo_return_1_grupo(get_token, create_5_groups):
    url = Endpoint.BASE_GROUP.value
    params = {
        "limit": 1
    }
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token), params=params)
    assert_status_code_200(response)
    json_response = response.json()
    tam_grupos = len(json_response.get("data", []))
    assert tam_grupos == 1, f"El tamaño de la lista de grupos ({tam_grupos}) no coincide con el limit (1)"
    assert_valid_schema(json_response, GROUPS_SCHEMA_BODY)


@pytest.mark.positivas
@pytest.mark.humo
def test_solicitar_limit_maximo_return_todos_grupos(get_token, create_5_groups):
    url = Endpoint.BASE_GROUP.value
    params = {
        "limit": 10000
    }
    response = BagistoRequest.get(url, headers=get_auth_headers(get_token), params=params)
    assert_status_code_200(response)
    json_response = response.json()
    tam_grupos = len(json_response.get("data", []))
    assert tam_grupos == json_response["meta"]["total"], f"El tamaño de la lista de grupos ({tam_grupos}) no coincide con el total de grupos ({json_response['meta']['total']})"
    assert_valid_schema(json_response, GROUPS_SCHEMA_BODY)
