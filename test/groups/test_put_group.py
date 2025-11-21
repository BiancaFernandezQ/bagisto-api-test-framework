import pytest
from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_401, assert_status_code_404, assert_status_code_400
import time
from src.schemas.groups.groups_schemas import GROUPS_SCHEMA_BODY, GROUP_SCHEMA_IND, CREATE_BODY_GROUP_SCHEMA, GROUPS_PAYLOAD_SCHEMA
from src.assertions.response_assertions import assert_valid_schema, assert_response_contiene_data_y_meta, assert_content_type_es_json, assert_response_contiene_campo
from src.helpers.groups_helper import GroupHelper
from src.services.group_service import GroupService

@pytest.mark.humo
@pytest.mark.positivas
@pytest.mark.actualizar_grupo
def test_actulizar_grupo_existente_valido_return_200(get_token, group_teardown):
    grupo_creado = GroupHelper.create_random_group(get_token)
    assert_status_code_200(grupo_creado)
    grupo_id = grupo_creado.json()["data"]["id"]
    group_teardown.append(grupo_id)
    grupo_datos = GroupHelper.create_grupo_data(name=None, code=None)
    response = GroupService.update_group(get_token, grupo_id, grupo_datos)
    assert_valid_schema(grupo_datos, GROUPS_PAYLOAD_SCHEMA)
    assert_status_code_200(response)
    json_response = response.json()
    assert_valid_schema(json_response, CREATE_BODY_GROUP_SCHEMA )
    assert_response_contiene_campo(json_response, "message")
    assert_response_contiene_campo(json_response, "data")
    assert json_response["data"]["id"] == grupo_id
    assert json_response["data"]["name"] == grupo_datos["name"]
    assert_content_type_es_json(response)

@pytest.mark.negativas
@pytest.mark.regresion
@pytest.mark.actualizar_grupo
def test_actualizar_grupo_id_no_existente_return_404(get_token):
    id_inexistente = 999999
    grupo_datos = GroupHelper.create_grupo_data(name=None, code=None)
    response = GroupService.update_group(get_token, id_inexistente, grupo_datos)
    assert_status_code_404(response)

@pytest.mark.positivas
@pytest.mark.humo
@pytest.mark.actualizar_grupo
def test_verificar_updated_at_se_actualice_al_actualizar_grupo(get_token, group_teardown):
    grupo_creado = GroupHelper.create_random_group(get_token)
    assert_status_code_200(grupo_creado)
    time.sleep(2)

    grupo_id = grupo_creado.json()["data"]["id"]
    group_teardown.append(grupo_id)
    
    updated_at_antes = grupo_creado.json()["data"]["updated_at"]
    grupo_datos = GroupHelper.create_grupo_data(name=None, code=None)
    response = GroupService.update_group(get_token, grupo_id, grupo_datos)
    assert_status_code_200(response)
    json_response = response.json()
    updated_at_despues = json_response["data"]["updated_at"]
    assert_valid_schema(grupo_datos, GROUPS_PAYLOAD_SCHEMA) 
    assert_valid_schema(json_response, CREATE_BODY_GROUP_SCHEMA) 
    assert updated_at_antes != updated_at_despues, "El campo updated_at no se actualizó correctamente"
    assert_content_type_es_json(response)

@pytest.mark.positivas
@pytest.mark.humo
@pytest.mark.actualizar_grupo
def test_verificar_created_at_no_se_actualice_al_actualizar_grupo(get_token, group_teardown):
    grupo_creado = GroupHelper.create_random_group(get_token) #crear grupo primero
    assert_status_code_200(grupo_creado)
    grupo_id = grupo_creado.json()["data"]["id"]
    group_teardown.append(grupo_id)
    created_at_antes = grupo_creado.json()["data"]["created_at"]

    time.sleep(2)
    
    grupo_datos = GroupHelper.create_grupo_data(name=None, code=None)
    response = GroupService.update_group(get_token, grupo_id, grupo_datos)
    assert_status_code_200(response)
    json_response = response.json()
    created_at_despues = json_response["data"]["created_at"]
    assert_valid_schema(grupo_datos, GROUPS_PAYLOAD_SCHEMA) #vrificar lo que enviamos
    assert_valid_schema(json_response, CREATE_BODY_GROUP_SCHEMA)  #verificar lo que recibimos
    assert created_at_antes == created_at_despues, "El campo created_at se modificó al actualizar el grupo"
    assert_content_type_es_json(response)

@pytest.mark.negativas
@pytest.mark.regresion
@pytest.mark.actualizar_grupo
def test_actualizar_grupo_payload_vacio_return_400(get_token, group_teardown):
    grupo_creado = GroupHelper.create_random_group(get_token)
    assert_status_code_200(grupo_creado)
    grupo_id = grupo_creado.json()["data"]["id"]
    group_teardown.append(grupo_id)
    grupo_datos = {}
    response = GroupService.update_group(get_token, grupo_id, grupo_datos)
    assert_status_code_400(response)

@pytest.mark.negativas
@pytest.mark.regresion
@pytest.mark.actualizar_grupo
def test_verificar_que_no_se_actualice_grupo_si_name_vacio(get_token, group_teardown):
    grupo_creado = GroupHelper.create_random_group(get_token)
    assert_status_code_200(grupo_creado)
    time.sleep(1)
    grupo_original = grupo_creado.json()["data"]["name"]
    grupo_id = grupo_creado.json()["data"]["id"]
    group_teardown.append(grupo_id)
    grupo_datos = {
        "code": ""
    }
    response = GroupService.update_group(get_token, grupo_id, grupo_datos)
    assert_status_code_400(response)
    grupo_consultado = GroupService.get_group_by_id(get_token, grupo_id)
    assert_status_code_200(grupo_consultado)
    assert grupo_consultado.json()["data"]["code"] == grupo_original

@pytest.mark.negativas
@pytest.mark.humo
@pytest.mark.actualizar_grupo
def test_verificar_que_no_se_actualice_el_grupo_por_defecto(get_token):
    grupo_id = 1  #ID del grupo por defecto
    grupo_datos = GroupHelper.create_grupo_data(name=None, code=None)
    response = GroupService.update_group(get_token, grupo_id, grupo_datos)
    assert_status_code_400(response)