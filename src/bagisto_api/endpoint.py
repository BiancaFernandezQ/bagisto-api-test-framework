from enum import Enum
from config.config import BASE_URI


class Endpoint(Enum):
    BASE_CUSTOMER = f"{BASE_URI}/admin/customers"
    #BASE_GROUPS = f"{BASE_URI}/" 
