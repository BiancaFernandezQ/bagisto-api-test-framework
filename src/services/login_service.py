from src.bagisto_api.api_request import BagistoRequest
from src.bagisto_api.endpoint import Endpoint
from src.utils.logger import setup_logger

logger = setup_logger("login_service")

class LoginService:
    @staticmethod
    def login_admin(email, password, device_name="ci-test"):
        logger.info(f"Iniciando proceso de login para el usuario: {email}")
        url = "http://localhost:8000/api/v1/admin/login"
        payload = {"email": email, "password": password, "device_name": device_name}
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        return BagistoRequest.post(url, headers=headers, json=payload)
