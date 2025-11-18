from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_401, assert_status_code_404, assert_status_code_400
from src.schemas.customers.customer import CUSTOMER_SCHEMA, CUSTOMER_SCHEMA_IND, CUSTOMER_POST_RESPONSE_SCHEMA, CUSTOMER_PAYLOAD_SCHEMA, CUSTOMER_EDIT_PAYLOAD_SCHEMA
from src.bagisto_api.api_request import BagistoRequest
from src.assertions.response_assertions import assert_valid_schema, assert_response_contiene_data_y_meta, assert_response_contiene_campo
from src.bagisto_api.endpoint import Endpoint
from src.helpers.customer_helper import CustomerHelper
from src.services.customer_service import CustomerService
import pytest
import time

@pytest.mark.positivas
@pytest.mark.humo
@pytest.mark.eliminar_cliente
def test_eliminar_cliente_id_existente_return_200(get_token):
    response_create = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(response_create)
    cliente_id = response_create.json()["data"]["id"]
    time.sleep(1) 
    response = CustomerService.delete_customer(get_token, cliente_id)
    assert_status_code_200(response)
    json_response = response.json()
    assert_response_contiene_campo(json_response, "message")
    assert json_response["message"] == "Customer successfully deleted"

@pytest.mark.negativas
@pytest.mark.regresion
@pytest.mark.eliminar_cliente
def test_eliminar_cliente_id_no_existente_return_404(get_token):
    id_inexistente = 999999
    response = CustomerService.delete_customer(get_token, id_inexistente)
    assert_status_code_404(response)

@pytest.mark.negativas
@pytest.mark.humo
@pytest.mark.eliminar_cliente
def test_eliminar_cliente_dos_veces_return_404(get_token):
    response_create = CustomerHelper.create_random_customer(get_token)
    assert_status_code_200(response_create)
    cliente_id = response_create.json()["data"]["id"]
    time.sleep(1)
    primer_delete = CustomerService.delete_customer(get_token, cliente_id)
    assert_status_code_200(primer_delete)

    segundo_delete = CustomerService.delete_customer(get_token, cliente_id)
    assert_status_code_404(segundo_delete)

@pytest.mark.eliminar_cliente
@pytest.mark.negativas
@pytest.mark.humo
def test_eliminar_cliente_con_token_expirado_return_401(get_token):
    # Usamos un ID cualquiera, ya que la autenticación fallará antes.
    response = CustomerService.delete_customer("20|65468485548484488481", 123)
    assert_status_code_401(response)
