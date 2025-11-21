import pytest
from src.services.login_service import LoginService
from src.assertions.status_code_assertion import assert_status_code_200, assert_status_code_422
from src.assertions.response_assertions import assert_response_contiene_campo, assert_valid_schema
from config.config import ADMIN_EMAIL, ADMIN_PASSWORD
from faker import Faker

fake = Faker()

from src.schemas.login.login_schema import LOGIN_SUCCESS_SCHEMA, LOGIN_ERROR_SCHEMA, LOGIN_EMAIL_INVALID_SCHEMA

@pytest.mark.positivas
@pytest.mark.humo
@pytest.mark.login
def test_auth_exitoso_con_credenciales_validas():
    response = LoginService.login_admin(ADMIN_EMAIL, ADMIN_PASSWORD)
    assert_status_code_200(response)
    json_response = response.json()
    assert_response_contiene_campo(json_response, "message")
    assert_response_contiene_campo(json_response, "data")
    assert_response_contiene_campo(json_response, "token")
    assert json_response["message"] == "Logged in successfully."
    assert_valid_schema(json_response, LOGIN_SUCCESS_SCHEMA)

@pytest.mark.negativas
@pytest.mark.humo
@pytest.mark.login
def test_auth_fallido_con_credenciales_invalidas():
    response = LoginService.login_admin("admi2ns@example.com", "asdassda")
    assert_status_code_422(response)
    json_response = response.json()
    assert_valid_schema(response.json(), LOGIN_ERROR_SCHEMA)
    assert_response_contiene_campo(response.json(), "message")
    assert_response_contiene_campo(response.json(), "errors")
    assert json_response["message"] == "The provided credentials are incorrect."

@pytest.mark.negativas
@pytest.mark.regresion
@pytest.mark.login
def test_auth_fallido_con_email_invalido():
    response = LoginService.login_admin("email-invalido", ADMIN_PASSWORD)
    assert_status_code_422(response)
    json_response = response.json()
    assert_valid_schema(response.json(), LOGIN_EMAIL_INVALID_SCHEMA)
    assert_response_contiene_campo(response.json(), "message")
    assert_response_contiene_campo(response.json(), "errors")
    assert json_response["message"] == "The email field must be a valid email address."

@pytest.mark.negativas
@pytest.mark.regresion
@pytest.mark.login
def test_auth_fallido_con_password_incorrecto():
    response = LoginService.login_admin(ADMIN_EMAIL, "password-incorrecta")
    assert_status_code_422(response)
    assert_valid_schema(response.json(), LOGIN_ERROR_SCHEMA)
    json_response = response.json()
    assert_response_contiene_campo(response.json(), "message")
    assert_response_contiene_campo(response.json(), "errors")
    assert json_response["message"] == "The provided credentials are incorrect." 

@pytest.mark.negativas
@pytest.mark.regresion
@pytest.mark.login
def test_auth_fallido_con_crendenciales_vacias():
    response = LoginService.login_admin("", "")
    assert_status_code_422(response)
    assert_response_contiene_campo(response.json(), "message")
    assert_response_contiene_campo(response.json(), "errors")
    assert_valid_schema(response.json(), LOGIN_ERROR_SCHEMA)


@pytest.mark.negativas
@pytest.mark.regresion
@pytest.mark.login
def test_auth_fallido_con_email_vacia_password_valido():
    response = LoginService.login_admin("", ADMIN_PASSWORD)
    assert_status_code_422(response)
    assert_response_contiene_campo(response.json(), "message")
    assert_response_contiene_campo(response.json(), "errors")
    assert_valid_schema(response.json(), LOGIN_ERROR_SCHEMA)
    json_response = response.json()
    assert json_response["message"] == "The email field is required."

@pytest.mark.negativas
@pytest.mark.regresion
@pytest.mark.login
def test_auth_fallido_con_password_vacia_email_valido():
    response = LoginService.login_admin(ADMIN_EMAIL, "")
    assert_status_code_422(response)
    assert_response_contiene_campo(response.json(), "message")
    assert_response_contiene_campo(response.json(), "errors")
    assert_valid_schema(response.json(), LOGIN_ERROR_SCHEMA)
    json_response = response.json()
    assert json_response["message"] == "The password field is required."
