def get_auth_headers(token: str, extra_headers: dict = None) -> dict:
    headers = {
        "Authorization": f"Bearer {token}"
    }
    if extra_headers:
        headers.update(extra_headers)
    return headers