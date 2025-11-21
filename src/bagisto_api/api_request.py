import requests
import datetime
import logging
from src.utils.logger import setup_logger

logger = setup_logger('api_request', level=logging.DEBUG)


class BagistoRequest:
    @staticmethod
    def get(url, headers=None, params=None):
        try:
            headers = headers or {}  # Si headers es None, asignar un diccionario vacío
            logger.info(f"Timestamp: {datetime.datetime.now(datetime.timezone.utc).isoformat()}") #Info timestamp de la request
            logger.info(f"Domain: {url.split('/api/v1')[0]}") #Info del dominio base
            logger.debug(f"Authentication: {headers.get('Authorization', 'No Auth')}") #Debug de la autenticación
            logger.debug(f"Request URL: GET {url} | Headers: {headers} | Params: {params}") #Debug de la URL, headers y params
            response = requests.get(url, headers=headers, params=params)
            logger.info(f"Status Code: {response.status_code}") #Info del status code
            #logger.debug(f"Response Payload: {response.text}") #Debug del payload de la respuesta
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"GET Request failed: {e}") #Error en caso de fallo en la request
            raise

    @staticmethod
    def post(url, headers, data=None, json=None):
        try:
            logger.info(f"Timestamp: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
            logger.info(f"Domain: {url.split('/api/v1')[0]}")
            logger.debug(f"Authentication: {headers.get('Authorization', 'No Auth')}")
            logger.debug(f"Request URL: POST {url} | Headers: {headers} | JSON: {json}")
            response = requests.post(url, headers=headers, data=data, json=json)
            logger.info(f"Status Code: {response.status_code}")
            #logger.debug(f"Response Payload: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"POST Request failed: {e}")
            raise

    @staticmethod
    def put(url, headers, json=None):
        try:
            logger.info(f"Timestamp: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
            logger.info(f"Domain: {url.split('/api/v1')[0]}")
            logger.debug(f"Authentication: {headers.get('Authorization', 'No Auth')}")
            logger.debug(f"Request URL: PUT {url} | Headers: {headers} | JSON: {json}")
            response = requests.put(url, headers=headers, json=json)
            logger.info(f"Status Code: {response.status_code}")
            #logger.debug(f"Response Payload: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"PUT Request failed: {e}")
            raise

    @staticmethod
    def delete(url, headers, data=None):
        try:
            logger.info(f"Timestamp: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
            logger.info(f"Domain: {url.split('/api/v1')[0]}")
            logger.debug(f"Authentication: {headers.get('Authorization', 'No Auth')}")
            logger.debug(f"Request URL: DELETE {url} | Headers: {headers}")
            response = requests.delete(url, headers=headers, data=data)
            logger.info(f"Status Code: {response.status_code}")
            #logger.debug(f"Response Payload: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"DELETE Request failed: {e}")
            raise
