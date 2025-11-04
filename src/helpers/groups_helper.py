from faker import Faker
from src.services.group_service import GroupService
Faker.locale = 'es_ES'
import json
import time

class GroupHelper:

    @staticmethod
    def create_random_group(token):
        group_data = {
            "code": Faker().unique.word().capitalize(),
            "name": Faker().company(),
        }
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
            "name": name or Faker().company(),
            "code": code or Faker().unique.word().capitalize(),
        }
        return grupo_data