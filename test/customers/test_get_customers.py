import os
import requests
import pytest
from config.config import BASE_URI
from src.assertions.status_code_assertion import assert_status_code_200
import json
import jsonschema
from src.schemas.customers.customer import CUSTOMER_SCHEMA
from src.bagisto_api.api_request import BagistoRequest
from src.assertions.customer.response_assertions import assert_valid_schema
from src.bagisto_api.endpoint import Endpoint

# test autenticado, obtener clientes
def test_autenticado_obtener_clientes_return_200(get_token):
    url = Endpoint.BASE_CUSTOMER.value
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    response = BagistoRequest.get(url, headers=headers)

    assert_status_code_200(response)
    
    json_data = response.json()

    assert "data" in json_data, "No se encontró el campo 'data'"
    assert isinstance(json_data["data"], list), "'data' no es una lista"
    assert "meta" in json_data, "No se encontró el campo 'meta'"
    assert "total" in json_data["meta"], "No se encontró el campo 'meta.total'"
    
    print("Respuesta JSON completa:", json_data)
    assert_valid_schema(json_data, CUSTOMER_SCHEMA)
    

def test_no_autenticado_obtener_clientes_return_500():
    url = Endpoint.BASE_CUSTOMER.value
    response = BagistoRequest.get(url)
    assert response.status_code == 500, f"Se esperaba 500 pero se obtuvo {response.status_code}"

def test_token_expirado_obtener_clientes_return_401(get_token):
    url = Endpoint.BASE_CUSTOMER.value
    headers = {"Authorization": "Bearer expired_or_invalid_token"}
    response = BagistoRequest.get(url, headers=headers)
    assert response.status_code == 401, f"Se esperaba 401 pero se obtuvo {response.status_code}"

#! test obtener clientes sin filtros, sin paginacion
#Verificar que la API devuelva una lista de clientes sin ningún filtro ni paginación.
def test_obtener_todos_clientes_sin_filtros_ni_paginacion(get_token):
    url = Endpoint.BASE_CUSTOMER.value
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    response = BagistoRequest.get(url, headers=headers)
    
    assert_status_code_200(response)
    
    json_response = response.json()
    #!precondicion clientes creados 10
    assert_valid_schema(json_response, CUSTOMER_SCHEMA)
    
    assert "data" in json_response, "No se encontró el campo 'data'"
    assert "meta" in json_response, "No se encontró el campo 'meta'"
    assert len(json_response.get("data", [])) <=10
    assert response.json()["meta"]["current_page"] == 1 # Verificar que la página actual sea 1 por defecto

#! obtener clientes con paginacion
# verificar que la API soporte paginacion cuando se proporciona el parametro page
def test_obtener_clientes_con_paginacion(get_token):
    url = Endpoint.BASE_CUSTOMER.value
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    #!pre condicion: tener minimo 12 clientes
    params = {
        "limit": 3,
        "page": 2  
    }
    response = BagistoRequest.get(url, headers=headers, params=params)
    assert_status_code_200(response)
    json_response = response.json()
    assert_valid_schema(json_response, CUSTOMER_SCHEMA)

    tam_clientes = len(json_response.get("data", []))
    #data debe tener el tamaño de limit
    assert tam_clientes == params["limit"], f"El tamaño de la lista de clientes ({tam_clientes}) no coincide con el limit ({params['limit']})"
    assert json_response["meta"]["current_page"] == params["page"], f"La página respuesta no coincide con la solicitada ({params['page']})"

# Consultar un cliente específico por su ID
def test_consultar_cliente_por_id(get_token):
    cliente_id = 10  #!Reemplaza con un ID de cliente válido para la prueba
    url = f"{Endpoint.BASE_CUSTOMER.value}?id={cliente_id}"
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    response = BagistoRequest.get(url, headers=headers)
    json_response = response.json()
    assert_status_code_200(response)
    assert "data" in json_response, "No se encontró el campo 'data'"
    assert len(json_response["data"]) == 1, "No se encontraron clientes con el ID proporcionado"
    assert json_response["data"][0]["id"] == cliente_id, f"El ID del cliente no coincide con el solicitado ({cliente_id})"
    assert_valid_schema(json_response, CUSTOMER_SCHEMA)

# Consultar clientes ordenados por ID y en orden ascendente
# Consultar clientes ordenados por ID y en orden descendente (por defecto)
@pytest.mark.parametrize("sort, order", [
    ("id", "asc"),
    ("id", "desc"),
])
@pytest.mark.prueba
def test_consultar_clientes_ordenados(get_token, sort, order):
    url = f"{Endpoint.BASE_CUSTOMER.value}?sort={sort}&order={order}"
    headers = {"Authorization": f"Bearer {get_token}"}
    
    response = BagistoRequest.get(url, headers=headers)
    assert_status_code_200(response)
    
    clientes = response.json()["data"]
    assert clientes == sorted(clientes, key=lambda x: x["id"], reverse=(order == "desc"))