def assert_status_code_200(response):
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

def assert_status_code_204(response):
    assert response.status_code == 204, f"Expected status code 500, but got {response.status_code}"

def assert_status_code_401(response):
    assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}"

def assert_status_code_400(response):
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"

def assert_status_code_404(response):
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"

def assert_status_code_422(response):
    assert response.status_code == 422, f"Expected status code 422, but got {response.status_code}"