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

    @staticmethod
    def delete_customer(token, customer_id):
        logger.info(f"Empezando el proceso para eliminar cliente con ID: {customer_id}")
        url = f"{Endpoint.BASE_CUSTOMER.value}/{customer_id}"
        return BagistoRequest.delete(url, headers=get_auth_headers(token))
    
    @staticmethod
    def update_customer(token, customer_id, payload):
        logger.info(f"Empezando el proceso para actualizar cliente con ID: {customer_id}")
        url = f"{Endpoint.BASE_CUSTOMER.value}/{customer_id}"
        return BagistoRequest.put(url, headers=get_auth_headers(token), json=payload)

    @staticmethod
    def get_customer_by_id(token, customer_id):
        logger.info(f"Empezando el proceso para obtener cliente con ID: {customer_id}")
        url = f"{Endpoint.BASE_CUSTOMER.value}/{customer_id}"
        return BagistoRequest.get(url, headers=get_auth_headers(token))

    @staticmethod
    def get_all_customers(token, params=None):
        logger.info(f"Empezando el proceso para obtener todos los clientes con parámetros: {params}")
        url = Endpoint.BASE_CUSTOMER.value
        return BagistoRequest.get(url, headers=get_auth_headers(token), params=params)
