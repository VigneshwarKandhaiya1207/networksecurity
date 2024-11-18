import os
import sys
from src.networksecurity.logger.logger import logger
from src.networksecurity.exception.exception import NetworkSecurityException
from src.networksecurity.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig
from src.networksecurity.components.data_ingestion import DataIngestion
from src.networksecurity.components.data_validation import DataValidation

if __name__=="__main__":
    logger.info("STAGE <<<<<<<<<<<< Initializing Training Pipeline Config >>>>>>>>>>>>")
    training_pipeline_config=TrainingPipelineConfig()
    logger.info("STAGE <<<<<<<<<<<< Initiatized Pipeline Config Sucessessfully >>>>>>>>>>>>")

    logger.info("STAGE <<<<<<<<<<<< Initializing the Dataingestion Config >>>>>>>>>>>>")
    data_ingestion_config=DataIngestionConfig(training_pipeline_config)
    logger.info("STAGE <<<<<<<<<<<< Initialized the Dataingestion Config Successfully >>>>>>>>>>>>")

    logger.info("STAGE <<<<<<<<<<<< Initiating Dataingestion Pipeline >>>>>>>>>>>>")
    data_ingestion=DataIngestion(data_ingestion_config)

    logger.info("STAGE <<<<<<<<<<<< Initiating the data Ingestion and archiving artifacts >>>>>>>>>>>>")
    data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
    logger.info("STAGE <<<<<<<<<<<< Data Ingestion Completed >>>>>>>>>>>>")

    logger.info("STAGE <<<<<<<<<<<< Initializing the Data Validation Config >>>>>>>>>>>>")
    data_validation_config=DataValidationConfig(training_pipeline_config)
    logger.info("STAGE <<<<<<<<<<<< Initialized the Data Validation Config Successfully >>>>>>>>>>>>")

    logger.info("STAGE <<<<<<<<<<<< Initiating Data Validation Pipeline >>>>>>>>>>>>")
    data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
    
    logger.info("STAGE <<<<<<<<<<<< Initiating the data validation and archiving artifacts >>>>>>>>>>>>")
    data_validation_artifact=data_validation.initiate_data_validation()
    print(data_validation_artifact)
    logger.info("STAGE <<<<<<<<<<<< Data Validation Completed >>>>>>>>>>>>")

