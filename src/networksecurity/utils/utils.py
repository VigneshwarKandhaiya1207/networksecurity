import os
import sys
from src.networksecurity.logger.logger import logger
from src.networksecurity.exception.exception import NetworkSecurityException


def create_directories(dir_name: list):
    try:
        for dir in dir_name:
            logger.info("Creating the directory {}".format(dir))
            os.makedirs(dir,exist_ok=True)
            logger.info("Directory {} created successfully.".format(dir))
    except Exception as e:
        raise NetworkSecurityException(e,sys)

