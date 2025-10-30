from src.bagisto_api.api_request import BagistoRequest
from src.bagisto_api.endpoint import Endpoint

class CustomerService:
    #Servicio de capa para interactuar con los endpoints de la API de clientes.
    @staticmethod
    def create_customer(token, customer_data):
        url = Endpoint.BASE_CUSTOMER.value
        headers = {"Authorization": f"Bearer {token}"}
        return BagistoRequest.post(url, headers=headers, json_data=customer_data)
