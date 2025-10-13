import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000/api/v1")
TOKEN = '2|m5piiDHgwkUPy5KGgP2JUBuqgYgPXa5wxZItzt0D34cf6765'

def test_get_admin_customers():
    """
    Test simple para validar el listado de clientes en Bagisto Admin.
    """
    url = f"{BASE_URL}/admin/customers"
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    response = requests.get(url, headers=headers)
    print('Response:', response.text)  # Depuración adicional
    # Verificaciones básicas
    assert response.status_code == 200, f"Status inesperado: {response.status_code}"
    json_data = response.json()

    # Validaciones simples
    assert isinstance(json_data, dict), "La respuesta no es un JSON válido"
    assert "data" in json_data, "No se encontró el campo 'data' en la respuesta"
    print(f"Clientes retornados: {len(json_data['data'])}")
