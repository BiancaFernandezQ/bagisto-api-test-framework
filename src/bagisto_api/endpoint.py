from enum import Enum
from config.config import BASE_URI


class Endpoint(Enum):
    BASE_LOGIN = f"{BASE_URI}/admin/login"
    BASE_CUSTOMER = f"{BASE_URI}/admin/customers"
    BASE_GROUP = f"{BASE_URI}/admin/customers/groups"
