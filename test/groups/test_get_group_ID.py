import pytest
from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_401, assert_status_code_404, assert_status_code_400
from src.schemas.groups.groups_schemas import GROUP_SCHEMA_IND
from src.assertions.response_assertions import assert_valid_schema, assert_content_type_es_json, assert_response_contiene_data
from src.helpers.groups_helper import GroupHelper
from src.services.group_service import GroupService

@pytest.mark.listar_grupo_especifico
@pytest.mark.positivas
@pytest.mark.humo
def test_consultar_grupo_por_id_return_200(get_token, create_group):
    grupo_id = create_group["data"]["id"]
    response = GroupService.get_group_by_id(get_token, grupo_id)
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
    response = GroupService.get_group_by_id(get_token, id_inexistente)
    assert_status_code_404(response)

@pytest.mark.listar_grupo_especifico
@pytest.mark.negativas
@pytest.mark.regresion
def test_consultar_grupo_con_id_no_entero_return_400(get_token):
    id_invalido = "abc#"
    response = GroupService.get_group_by_id(get_token, id_invalido)
    assert_status_code_400(response)

@pytest.mark.listar_grupo_especifico
@pytest.mark.negativas
@pytest.mark.regresion
def test_consultar_grupo_con_id_negativos_return_404(get_token):
    id_invalido = -10
    response = GroupService.get_group_by_id(get_token, id_invalido)
    assert_status_code_404(response)

@pytest.mark.listar_grupo_especifico
@pytest.mark.negativas
@pytest.mark.humo
def test_consultar_grupo_sin_token_return_401(create_group):
    grupo_id = create_group["data"]["id"]
    response = GroupService.get_group_by_id(None, grupo_id)
    assert_status_code_401(response)

@pytest.mark.listar_grupo_especifico
@pytest.mark.negativas
@pytest.mark.humo
def test_consultar_grupo_con_token_expirado_return_401(create_group):
    grupo_id = create_group["data"]["id"]
    response = GroupService.get_group_by_id("95|JU9nP77BVdVL5HfpV0UTNP4ZbvZ4VkrLeURmY8pjd", grupo_id)
    assert_status_code_401(response)

@pytest.mark.listar_grupo_especifico
@pytest.mark.positivas
@pytest.mark.regresion
def test_consultar_grupo_por_id_response_json(get_token, create_group):
    grupo_id = create_group["data"]["id"]
    response = GroupService.get_group_by_id(get_token, grupo_id)
    assert_status_code_200(response)
    assert_content_type_es_json(response)