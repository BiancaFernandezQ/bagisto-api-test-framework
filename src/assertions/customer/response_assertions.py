import jsonschema
import pytest
import src.utils.logger as logger

log = logger.setup_logger('assertions')

def assert_valid_schema(response_json, schema):
    log.info("Validando esquema JSON.")
    try:
        jsonschema.validate(instance=response_json, schema=schema)
        log.info("El esquema JSON es válido.")
    except jsonschema.exceptions.ValidationError as error:
        log.error(f"Fallo en la validación del esquema: {error}")
        pytest.fail(f'El esquema JSON no coincide: {error}')

def assert_response_contiene_data_y_meta(response_json):
    log.info("Verificando la presencia de 'data' y 'meta' en la respuesta.")
    assert_response_contiene_meta(response_json)
    assert_response_contiene_data(response_json)

def assert_content_type_es_json(response):
    log.info("Verificando que el Content-Type sea 'application/json'.")
    assert response.headers["Content-Type"] == "application/json", f"Content-Type esperado 'application/json', pero se recibió '{response.headers['Content-Type']}'"

def assert_data_es_una_lista(response_json):
    log.info("Verificando que el campo 'data' sea una lista.")
    assert isinstance(response_json["data"], list), f"Se esperaba que 'data' fuera una lista, pero es {type(response_json.get('data'))}"

def assert_response_total_en_meta(response_json):
    log.info("Verificando la presencia de 'total' en 'meta'.")
    assert "total" in response_json["meta"], "No se encontró el campo 'meta.total'"

def assert_response_contiene_meta(response_json):
    log.info("Verificando la presencia del campo 'meta'.")
    assert "meta" in response_json, "El campo 'meta' no se encuentra en la respuesta"

def assert_response_contiene_data(response_json):
    log.info("Verificando la presencia del campo 'data'.")
    assert "data" in response_json, "El campo 'data' no se encuentra en la respuesta"

def assert_response_contiene_campo(response_json, campo):
    log.info(f"Verificando la presencia del campo '{campo}'.")
    assert campo in response_json, f"El campo '{campo}' no se encuentra en la respuesta"

def assert_current_page_actual_es_1_por_defecto(response_json):
    log.info("Verificando que 'current_page' sea 1 por defecto.")
    assert response_json["meta"]["current_page"] == 1, f"Se esperaba que 'meta.current_page' fuera 1 por defecto, pero es {response_json['meta']['current_page']}"

def assert_current_page_es(response_json, pagina_esperada):
    log.info(f"Verificando que 'current_page' sea {pagina_esperada}.")
    pagina_actual = response_json["meta"]["current_page"]
    assert pagina_actual == pagina_esperada, f"Se esperaba que 'meta.current_page' fuera {pagina_esperada}, pero es {pagina_actual}"

def assert_created_at_en_response(response_json):
    log.info("Verificando la presencia del campo 'created_at' en la respuesta.")
    assert "created_at" in response_json["data"], "El campo 'created_at' no se encuentra en 'data'"

def assert_updated_at_en_response(response_json):
    log.info("Verificando la presencia del campo 'updated_at' en la respuesta.")
    assert "updated_at" in response_json["data"], "El campo 'updated_at' no se encuentra en 'data'"

def assert_data_no_es_nulo(response_json):
    log.info("Verificando que el campo 'data' no sea nulo.")
    assert response_json["data"] is not None, "El campo 'data' es nulo"