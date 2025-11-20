import pytest
from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_401, assert_status_code_404, assert_status_code_400
import time
from src.bagisto_api.api_request import BagistoRequest
from src.assertions.response_assertions import assert_response_contiene_campo, assert_content_type_es_json
from src.bagisto_api.endpoint import Endpoint
from src.helpers.groups_helper import GroupHelper
from src.helpers.customer_helper import CustomerHelper
from src.services.group_service import GroupService
from src.services.customer_service import CustomerService

@pytest.mark.positivas
@pytest.mark.humo
@pytest.mark.eliminar_grupo
def test_eliminar_grupo_valido_id_existente_return_200(get_token):
    response_create = GroupHelper.create_random_group(get_token)
    assert_status_code_200(response_create)
    grupo_id = response_create.json()["data"]["id"]
    time.sleep(2) 
    response = GroupService.delete_group(get_token, grupo_id)
    assert_status_code_200(response)
    json_response = response.json()
    assert_response_contiene_campo(json_response, "message")
    assert_content_type_es_json(response)
    assert json_response["message"] == "Customer group successfully deleted"

@pytest.mark.negativas
@pytest.mark.regresion
@pytest.mark.eliminar_grupo
def test_eliminar_grupo_id_no_existente_return_404(get_token):
    id_inexistente = 999999
    response = GroupService.delete_group(get_token, id_inexistente)
    assert_status_code_404(response)

@pytest.mark.negativas
@pytest.mark.humo
@pytest.mark.eliminar_grupo
def test_eliminar_grupo_con_token_expirado_return_401():
    response = GroupService.delete_group("20|65468485548484488481", 123)
    assert_status_code_401(response)

@pytest.mark.negativas
@pytest.mark.humo
@pytest.mark.eliminar_grupo
def test_eliminar_grupo_valido_dos_veces_return_404(get_token):
    response_create = GroupHelper.create_random_group(get_token)
    assert_status_code_200(response_create)
    grupo_id = response_create.json()["data"]["id"]
    time.sleep(1) 
    primer_delete = GroupService.delete_group(get_token, grupo_id)
    assert_status_code_200(primer_delete)

    segundo_delete = GroupService.delete_group(get_token, grupo_id)
    assert_status_code_404(segundo_delete)

@pytest.mark.negativas
@pytest.mark.humo
@pytest.mark.eliminar_grupo
def test_eliminar_grupo_con_clientes_asociados_return_400(get_token):
    response_create = GroupHelper.create_random_group(get_token)
    assert_status_code_200(response_create)
    grupo_id = response_create.json()["data"]["id"]
    time.sleep(1)
    customer_payload = CustomerHelper.create_customer_data(first_name=None, last_name=None, email=None, gender=None, customer_group_id=grupo_id)
    response_customer = CustomerService.create_customer(get_token, customer_payload)
    assert_status_code_200(response_customer)
    time.sleep(1) 
    response_delete = GroupService.delete_group(get_token, grupo_id)
    assert_status_code_400(response_delete)