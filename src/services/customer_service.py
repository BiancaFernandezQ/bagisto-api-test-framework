from src.bagisto_api.api_request import BagistoRequest
from src.bagisto_api.endpoint import Endpoint
from src.utils.auth import get_auth_headers
from src.utils.logger import setup_logger

logger = setup_logger("customer_service")

class CustomerService:
    #Servicio de capa para interactuar con los endpoints de la API de clientes.
    @staticmethod
    def create_customer(token, customer_data):
        logger.info("Empezando el proceso para crear cliente ")
        url = Endpoint.BASE_CUSTOMER.value
        return BagistoRequest.post(url, headers=get_auth_headers(token), json=customer_data)

    def delete_customer(token, customer_id):
        logger.info(f"Empezando el proceso para eliminar cliente con ID: {customer_id}")
        url = f"{Endpoint.BASE_CUSTOMER.value}/{customer_id}"
        return BagistoRequest.delete(url, headers=get_auth_headers(token))