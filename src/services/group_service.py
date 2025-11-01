from src.bagisto_api.api_request import BagistoRequest
from src.bagisto_api.endpoint import Endpoint

class GroupService:
    #Servicio de capa para interactuar con los endpoints de la API de grupos.
    @staticmethod
    def create_group(token, group_data):
        url = Endpoint.BASE_GROUP.value
        headers = {"Authorization": f"Bearer {token}"}
        return BagistoRequest.post(url, headers=headers, json=group_data)