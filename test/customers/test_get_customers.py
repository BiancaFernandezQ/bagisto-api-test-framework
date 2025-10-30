import os
import requests
import pytest
from config.config import BASE_URI
from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_401, assert_status_code_400
import json
import jsonschema
from src.schemas.customers.customer import CUSTOMER_SCHEMA
from src.bagisto_api.api_request import BagistoRequest
from src.assertions.customer.response_assertions import assert_valid_schema, assert_response_contiene_data_y_meta
from src.bagisto_api.endpoint import Endpoint

@pytest.mark.positivas
@pytest.mark.humo
# Verificar que un usuario autenticado pueda obtener la lista de clientes 
def test_autenticado_obtener_clientes_return_200(get_token, create_15_customers):
    url = Endpoint.BASE_CUSTOMER.value
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    response = BagistoRequest.get(url, headers=headers)
    
    assert_status_code_200(response)
    
    json_data = response.json()

    assert_response_contiene_data_y_meta(json_data)
    assert isinstance(json_data["data"], list), "'data' no es una lista"
    assert "total" in json_data["meta"], "No se encontró el campo 'meta.total'"
    
    print("Respuesta JSON completa:", json_data)
    assert_valid_schema(json_data, CUSTOMER_SCHEMA)

@pytest.mark.positivas
@pytest.mark.humo
#Verificar que la API devuelva una lista de clientes sin ningún filtro ni paginación.
def test_obtener_todos_clientes_sin_filtros_ni_paginacion(get_token, create_15_customers):
    url = Endpoint.BASE_CUSTOMER.value
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    response = BagistoRequest.get(url, headers=headers)
    
    assert_status_code_200(response)
    
    json_response = response.json()
    assert_valid_schema(json_response, CUSTOMER_SCHEMA)
    
    assert_response_contiene_data_y_meta(json_response)
    assert len(json_response.get("data", [])) <=10 # por defecto es 10
    assert response.json()["meta"]["current_page"] == 1 # Verificar que la página actual sea 1 por defecto

@pytest.mark.positivas
@pytest.mark.humo
# verificar que la API soporte paginacion cuando se proporciona el parametro page
def test_obtener_clientes_con_paginacion(get_token, create_15_customers):
    url = Endpoint.BASE_CUSTOMER.value
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
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

# Consultar clientes ordenados por ID y en orden ascendente
# Consultar clientes ordenados por ID y en orden descendente (pre establecido)
@pytest.mark.positivas
@pytest.mark.humo
@pytest.mark.parametrize("sort, order", [
    ("id", "asc"),
    ("id", "desc"),
])
def test_consultar_clientes_ordenados(get_token,create_15_customers, sort, order):
    url = f"{Endpoint.BASE_CUSTOMER.value}?sort={sort}&order={order}"
    headers = {"Authorization": f"Bearer {get_token}"}
    
    response = BagistoRequest.get(url, headers=headers)
    assert_status_code_200(response)
    
    clientes = response.json()["data"]
    assert clientes == sorted(clientes, key=lambda x: x["id"], reverse=(order == "desc"))

# Intentar obtener clientes sin token de autenticación
@pytest.mark.negativas
@pytest.mark.humo
#!como tal no es un bug pero me manda un 501 en vez de un 401, es una mala practica, recomendacion
def test_no_autenticado_obtener_clientes_return_401():
    url = Endpoint.BASE_CUSTOMER.value
    response = BagistoRequest.get(url)
    assert_status_code_401(response)

@pytest.mark.negativas
@pytest.mark.humo
#!como tal no es un bug pero me manda un 501 en vez de un 401, es una mala practica, recomendacion
# Intentar obtener clientes con un token expirado o inválido
def test_token_expirado_obtener_clientes_return_401(get_token):
    url = Endpoint.BASE_CUSTOMER.value
    headers = {"Authorization": "Bearer expired_or_invalid_token"}
    response = BagistoRequest.get(url, headers=headers)
    assert_status_code_401(response)

@pytest.mark.negativas
@pytest.mark.humo
def test_solicitar_page_inexistente_return_data_vacia(get_token, create_15_customers):
    url = Endpoint.BASE_CUSTOMER.value
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    params = {
        "limit": 10,
        "page": 9999  
    }
    response = BagistoRequest.get(url, headers=headers, params=params)
    assert_status_code_200(response)
    json_response = response.json()
    assert len(json_response.get("data", [])) == 0, "Se esperaba una lista vacía de clientes para una página inexistente"

#!como tal no es un bug pero me manda un 200 en vez de un 400 o 404, es una mala practica, recomendacion
@pytest.mark.negativas
@pytest.mark.humo
def test_solicitar_limit_cero_return_400(get_token):
    url = Endpoint.BASE_CUSTOMER.value
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    params = {
        "limit": 0
    }
    response = BagistoRequest.get(url, headers=headers, params=params)
    assert_status_code_400(response)

#verificar respuesta con valor invalido negativo en el parametro de limit
@pytest.mark.negativas
@pytest.mark.humo
#!como tal no es un bug pero me manda un 500 en vez de un 400 (solicitud incorrect), es una mala practica, recomendacion
def test_solicitar_limit_negativo_return_400(get_token):
    url = Endpoint.BASE_CUSTOMER.value
    headers = { "Authorization": f"Bearer {get_token}" }
    params = { "limit": -5 }
    response = BagistoRequest.get(url, headers=headers, params=params)
    assert_status_code_400(response)

@pytest.mark.positivas
@pytest.mark.humo
def test_solicitar_limit_minimo_return_1_cliente(get_token, create_15_customers):
    url = Endpoint.BASE_CUSTOMER.value
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    params = {
        "limit": 1
    }
    response = BagistoRequest.get(url, headers=headers, params=params)
    assert_status_code_200(response)
    json_response = response.json()
    tam_clientes = len(json_response.get("data", []))
    assert tam_clientes == 1, f"El tamaño de la lista de clientes ({tam_clientes}) no coincide con el limit (1)"

@pytest.mark.positivas
@pytest.mark.humo
def test_solicitar_limit_maximo_return_todos_clientes(get_token, create_15_customers):
    url = Endpoint.BASE_CUSTOMER.value
    headers = {
        "Authorization": f"Bearer {get_token}"
    }
    params = {
        "limit": 10000
    }
    response = BagistoRequest.get(url, headers=headers, params=params)
    assert_status_code_200(response)
    json_response = response.json()
    tam_clientes = len(json_response.get("data", []))
    #tam_clientes debe ser igual al total de meta
    assert tam_clientes == json_response["meta"]["total"], f"El tamaño de la lista de clientes ({tam_clientes}) no coincide con el total de clientes"


# verificar respuesta con valor invalido en el parametro de order
@pytest.mark.negativas
@pytest.mark.humo
#!como tal no es un bug pero me manda un 500 en vez de un 400 (solicitud incorrect), es una mala practica, recomendacion
def test_solicitar_order_invalido_return_400(get_token):
    url = f"{Endpoint.BASE_CUSTOMER.value}?sort=id&order=invalid_order"
    headers = {"Authorization": f"Bearer {get_token}"}
    response = BagistoRequest.get(url, headers=headers)
    assert_status_code_400(response)

@pytest.mark.negativas
@pytest.mark.humo
# TC: Verificar respuesta con campo invalido en el parametro de sort 
#!como tal no es un bug pero me manda un 500 en vez de un 400 (solicitud incorrect), es una mala practica, recomendacion
def test_solicitar_sort_campo_inexistente_return_400(get_token):
    url = f"{Endpoint.BASE_CUSTOMER.value}?sort=no_valido&order=asc"
    headers = {"Authorization": f"Bearer {get_token}"}
    response = BagistoRequest.get(url, headers=headers)
    assert_status_code_400(response)


@pytest.mark.positivas
@pytest.mark.regresion
#Verificar que meta.total es consistente y refleja el total real de registros
def test_validar_consistencia_meta_total(get_token, create_15_customers):
    url = Endpoint.BASE_CUSTOMER.value
    headers = {"Authorization": f"Bearer {get_token}"}
    
    total_clientes = 0
    page = 1
    limit = 10 
    
    while True:
        response = BagistoRequest.get(url, headers=headers, params={"page": page, "limit": limit})
        assert_status_code_200(response)
        
        json_response = response.json()
        data = json_response.get("data", [])
        
        total_clientes += len(data)
        
        if not data:
            break
        
        page += 1
    
    page_uno = BagistoRequest.get(url, headers=headers, params={"limit": limit})
    meta_total = page_uno.json()["meta"]["total"]
    print(f"Total de clientes contados: {total_clientes}, meta.total: {meta_total}")
    assert total_clientes == meta_total, f"Total real ({total_clientes}) no coincide con meta.total ({meta_total})"
