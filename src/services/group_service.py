from src.bagisto_api.api_request import BagistoRequest
from src.bagisto_api.endpoint import Endpoint
from src.utils.auth import get_auth_headers
from src.utils.logger import setup_logger
logger = setup_logger("group_service")

class GroupService:
    #Servicio de capa para interactuar con los endpoints de la API de grupos.
    @staticmethod
    def create_group(token, group_data):
        logger.info(f"Empezando el proceso para crear grupo con datos: {group_data}")
        url = Endpoint.BASE_GROUP.value
        return BagistoRequest.post(url, headers=get_auth_headers(token), json=group_data)
    
    @staticmethod
    def delete_group(token, group_id):
        logger.info(f"Empezando el proceso para eliminar grupo con ID: {group_id}")
        url = f"{Endpoint.BASE_GROUP.value}/{group_id}"
        return BagistoRequest.delete(url, headers=get_auth_headers(token))

    @staticmethod
    def get_group_by_id(token, group_id):
        logger.info(f"Empezando el proceso para obtener grupo con ID: {group_id}")
        url = f"{Endpoint.BASE_GROUP.value}/{group_id}"
        return BagistoRequest.get(url, headers=get_auth_headers(token))

    @staticmethod
    def get_all_groups(token, params=None):
        logger.info(f"Empezando el proceso para obtener todos los grupos con parámetros: {params}")
        url = Endpoint.BASE_GROUP.value
        return BagistoRequest.get(url, headers=get_auth_headers(token), params=params)

    @staticmethod
    def update_group(token, group_id, payload):
        logger.info(f"Empezando el proceso para actualizar grupo con ID: {group_id}")
        url = f"{Endpoint.BASE_GROUP.value}/{group_id}"
        return BagistoRequest.put(url, headers=get_auth_headers(token), json=payload)