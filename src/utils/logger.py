import logging
import os
from logging.handlers import RotatingFileHandler

#ver menos detalles de logger level debe ser igual a 
def setup_logger(name, log_file='logs/combined.log', level=logging.WARNING):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(name)
    if not logger.handlers:
        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=2)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.setLevel(level)

    return logger


if __name__ == "__main__":
    logger = setup_logger('bagisto_API')
    logger.info("Logger configurado y listo para usar :)")
