from faker import Faker
from src.services.customer_service import CustomerService
Faker.locale = 'es_ES'
import json
import time
from src.utils.logger import setup_logger

logger = setup_logger('customer_helper')

class CustomerHelper:

    @staticmethod
    def create_random_customer(token):
        customer_data = {
            "first_name" : Faker().first_name(),
            "last_name" : Faker().last_name(), 
            "email" : Faker().email(),
            "gender" : Faker().random_element(['Male', 'Female', 'Other']),
            "customer_group_id" : 1,
        }
        logger.info(f"Creando cliente aleatorio con email: {customer_data['email']}")
        return CustomerService.create_customer(token, customer_data)
    
    @staticmethod
    def create_multiple_random_customers(token, count):
        responses = []
        for _ in range(count):
            response = CustomerHelper.create_random_customer(token)
            responses.append(response)
        return responses
    
    @staticmethod
    def create_customer_data(first_name, last_name, email, gender, customer_group_id=1,
                             date_of_birth=None, phone=None):
        unique_suffix = str(int(time.time() * 1000))
        customer_data = {
            "first_name" : first_name or Faker().first_name(),
            "last_name" : last_name or Faker().last_name(),
            "email" : email or Faker().email(),
            "gender": gender or Faker().random_element(['Male', 'Female', 'Other']),
            "customer_group_id" : customer_group_id,
        }
        if date_of_birth is not None:
            customer_data["date_of_birth"] = date_of_birth or Faker().date_of_birth(minimum_age=18, maximum_age=90).isoformat()
        if phone is not None:
            customer_data["phone"] = phone or Faker().random_number(digits=10, fix_len=True)
        
        logger.info(f"Construyendo cliente aleatorio con email: {customer_data['email']}")
        return customer_data

    def delete_customer(token, customer_id):
        logger.info(f"Eliminando cliente con ID: {customer_id}")
        return CustomerService.delete_customer(token, customer_id)