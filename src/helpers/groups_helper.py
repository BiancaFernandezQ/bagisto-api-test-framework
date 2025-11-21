from faker import Faker
from src.services.group_service import GroupService
Faker.locale = 'es_ES'
import json
import time
from src.utils.logger import setup_logger

logger = setup_logger('group_helper')


class GroupHelper:

    @staticmethod
    def create_random_group(token):
        group_data = {
            "code": f"{Faker().unique.word()}{int(time.time())}",
            "name": Faker().unique.word()
        }
        logger.info(f"Creando grupo aleatorio con code: {group_data['code']}")
        return GroupService.create_group(token, group_data)

    @staticmethod
    def create_multiple_random_groups(token, count):
        responses = []
        for _ in range(count):
            response = GroupHelper.create_random_group(token)
            responses.append(response)
        return responses

    @staticmethod
    def create_grupo_data(name=None, code=None):
        unique_suffix = str(int(time.time() * 1000))
        grupo_data = {
            #para que no repita en multiples llamadas
            "name": name or Faker().company() + "_" + unique_suffix,
            "code": code or Faker().unique.word().capitalize() + "_" + unique_suffix,
        }
        logger.info(f"Construyendo grupo aleatorio con code: {grupo_data['code']}")
        return grupo_data
    
    def delete_group(token, group_id):
        logger.info(f"Eliminando grupo con ID: {group_id}")
        return GroupService.delete_group(token, group_id)