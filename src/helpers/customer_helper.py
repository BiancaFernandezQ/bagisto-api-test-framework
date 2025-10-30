from faker import Faker
from src.services.customer_service import CustomerService
Faker.locale = 'es_ES'

class CustomerHelper:

    @staticmethod
    def create_random_customer(token):
        customer_data = {
            "first_name" : Faker().first_name(),
            "last_name" : Faker().last_name(), 
            "email" : Faker().email(),
            "gender" : Faker().random_element(['Male', 'Female']),
            "customer_group_id" : 1,
        }
        return CustomerService.create_customer(token, customer_data)
    
    @staticmethod
    def create_multiple_random_customers(token, count):
        responses = []
        for _ in range(count):
            response = CustomerHelper.create_random_customer(token)
            responses.append(response)
        return responses