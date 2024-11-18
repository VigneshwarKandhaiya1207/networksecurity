import os
import sys
from src.networksecurity.logger.logger import logger
from src.networksecurity.exception.exception import NetworkSecurityException
from src.networksecurity.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from src.networksecurity.components.data_ingestion import DataIngestion

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
