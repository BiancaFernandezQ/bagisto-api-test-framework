import jsonschema
import pytest

def assert_valid_schema(response_json, schema):
    #Valida que un JSON de respuesta cumpla con un esquema dado.
    try:
        jsonschema.validate(instance=response_json, schema=schema)
    except jsonschema.exceptions.ValidationError as error:
        pytest.fail(f'El esquema JSON no coincide: {error}')


