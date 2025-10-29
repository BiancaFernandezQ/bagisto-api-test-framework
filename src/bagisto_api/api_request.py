import requests
from src.utils.logger import setup_logger

logger = setup_logger('api_request')


class BagistoRequest:
    @staticmethod
    def get(url, headers=None, params=None):
        try:
            headers = headers or {}  # Si headers es None, asignar un diccionario vacío
            logger.info(f"GET Request URL: {url} | Headers: {headers} | Params: {params}")
            response = requests.get(url, headers=headers, params=params)
            logger.info(f"Response Status Code: {response.status_code}")
            logger.info(f"Response: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"GET Request failed: {e}")
            raise

    @staticmethod
    def post(url, headers, data):
        try:
            logger.info(f"POST Request URL: {url} | {headers}")
            response = requests.post(url, headers=headers, data=data)
            logger.info(f"Response Status Code: {response.status_code}")
            logger.info(f"Response: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"POST Request failed: {e}")
            raise

    @staticmethod
    def put(url, headers, data):
        try:
            logger.info(f"PUT Request URL: {url} | {headers}")
            response = requests.put(url, headers=headers, data=data)
            logger.info(f"Response Status Code: {response.status_code}")
            logger.info(f"Response: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"PUT Request failed: {e}")
            raise

    @staticmethod
    def delete(url, headers, data=None):
        try:
            logger.info(f"DELETE Request URL: {url} | {headers}")
            response = requests.delete(url, headers=headers, data=data)
            logger.info(f"Response Status Code: {response.status_code}")
            logger.info(f"Response: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"DELETE Request failed: {e}")
            raise
