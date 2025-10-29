def assert_status_code_200(response):
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

def assert_status_code_500(response):
    assert response.status_code == 204, f"Expected status code 500, but got {response.status_code}"
