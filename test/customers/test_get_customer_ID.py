import pytest
from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_401, assert_status_code_404, assert_status_code_400
from src.schemas.customers.customer import CUSTOMER_SCHEMA_IND
from src.assertions.response_assertions import assert_valid_schema, assert_response_contiene_data_y_meta, assert_content_type_es_json, assert_response_contiene_campo
from src.helpers.customer_helper import CustomerHelper
from src.services.customer_service import CustomerService

@pytest.mark.positivas
@pytest.mark.humo
@pytest.mark.listar_cliente_especifico
def test_consultar_cliente_por_id_return_200(get_token, create_customer):
    cliente_id = create_customer["data"]["id"]
    response = CustomerService.get_customer_by_id(get_token, cliente_id)
    json_response = response.json()
    assert_status_code_200(response)
    assert_content_type_es_json(response)
    assert_response_contiene_campo(json_response, "data")
    assert json_response["data"]["id"] == cliente_id, f"El ID del cliente no coincide con el solicitado ({cliente_id})"
    assert_valid_schema(json_response, CUSTOMER_SCHEMA_IND)


@pytest.mark.negativas
@pytest.mark.humo
@pytest.mark.listar_cliente_especifico
def test_consultar_cliente_con_id_inexistente_return_404(get_token):
    id_inexistente = 999999
    response = CustomerService.get_customer_by_id(get_token, id_inexistente)
    assert_status_code_404(response)

@pytest.mark.negativas
@pytest.mark.regresion
@pytest.mark.listar_cliente_especifico
def test_consultar_cliente_con_id_no_entero_return_400(get_token):
    id_invalido = "abc#"
    response = CustomerService.get_customer_by_id(get_token, id_invalido)
    assert_status_code_400(response)

@pytest.mark.negativas
@pytest.mark.regresion
@pytest.mark.listar_cliente_especifico
def test_consultar_cliente_con_id_negativos_return_404(get_token):
    id_invalido = -10
    response = CustomerService.get_customer_by_id(get_token, id_invalido)
    assert_status_code_404(response)

@pytest.mark.negativas
@pytest.mark.humo
@pytest.mark.listar_cliente_especifico
def test_consultar_cliente_sin_token_return_401(create_customer):
    cliente_id = create_customer["data"]["id"]
    response = CustomerService.get_customer_by_id(None, cliente_id)
    assert_status_code_401(response)

@pytest.mark.negativas
@pytest.mark.humo
@pytest.mark.listar_cliente_especifico
def test_consultar_cliente_con_token_expirado_return_401(create_customer):
    cliente_id = create_customer["data"]["id"]
    response = CustomerService.get_customer_by_id("95|JU9nP77BVdVL5HfpV0UTNP4ZbvZ4VkrLeURmY8pjd", cliente_id)
    assert_status_code_401(response)