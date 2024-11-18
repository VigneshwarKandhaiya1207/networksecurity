import os
import sys
import yaml
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

def read_yaml(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

def write_yaml(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)