import jsonschema
import pytest

def assert_valid_schema(response_json, schema):
    #Valida que un JSON de respuesta cumpla con un esquema dado.
    try:
        jsonschema.validate(instance=response_json, schema=schema)
    except jsonschema.exceptions.ValidationError as error:
        pytest.fail(f'El esquema JSON no coincide: {error}')


def assert_response_contiene_data_y_meta(response_json):
    assert "data" in response_json, "No se encontró el campo 'data'"
    assert "meta" in response_json, "No se encontró el campo 'meta'"

@staticmethod
def assert_field_value(response_json, field_path, expected_value):
    keys = field_path.split('.')
    actual_value = response_json
    for key in keys:
        actual_value = actual_value[key]
    assert actual_value == expected_value, f"Field '{field_path}' has value '{actual_value}', but '{expected_value}' was expected"