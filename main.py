import os
import sys
from src.networksecurity.logger.logger import logger
from src.networksecurity.exception.exception import NetworkSecurityException
from src.networksecurity.entity.config_entity import (TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,
                                                      DataTransformationConfig,ModelTrainerConfig)
from src.networksecurity.components.data_ingestion import DataIngestion
from src.networksecurity.components.data_validation import DataValidation
from src.networksecurity.components.data_transformation import DataTransformation
from src.networksecurity.components.model_trainer import ModelTrainer

if __name__=="__main__":
    logger.info("STAGE <<<<<<<<<<<< Initializing Training Pipeline Config >>>>>>>>>>>>")
    training_pipeline_config=TrainingPipelineConfig()
    logger.info("STAGE <<<<<<<<<<<< Initiatized Pipeline Config Sucessessfully >>>>>>>>>>>>")

    ################################## Data Ingestion ##################################


    logger.info("STAGE <<<<<<<<<<<< Initializing the Dataingestion Config >>>>>>>>>>>>")
    data_ingestion_config=DataIngestionConfig(training_pipeline_config)
    logger.info("STAGE <<<<<<<<<<<< Initialized the Dataingestion Config Successfully >>>>>>>>>>>>")

    logger.info("STAGE <<<<<<<<<<<< Initiating Dataingestion Pipeline >>>>>>>>>>>>")
    data_ingestion=DataIngestion(data_ingestion_config)

    logger.info("STAGE <<<<<<<<<<<< Initiating the data Ingestion and archiving artifacts >>>>>>>>>>>>")
    data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
    logger.info("STAGE <<<<<<<<<<<< Data Ingestion Completed >>>>>>>>>>>>")

    ################################## Data Validation ##################################

    logger.info("STAGE <<<<<<<<<<<< Initializing the Data Validation Config >>>>>>>>>>>>")
    data_validation_config=DataValidationConfig(training_pipeline_config)
    logger.info("STAGE <<<<<<<<<<<< Initialized the Data Validation Config Successfully >>>>>>>>>>>>")

    logger.info("STAGE <<<<<<<<<<<< Initiating Data Validation Pipeline >>>>>>>>>>>>")
    data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)

    logger.info("STAGE <<<<<<<<<<<< Initiating the data validation and archiving artifacts >>>>>>>>>>>>")
    data_validation_artifact=data_validation.initiate_data_validation()
    print(data_validation_artifact)
    logger.info("STAGE <<<<<<<<<<<< Data Validation Completed >>>>>>>>>>>>")

    ################################## Data Transformation ##################################

    logger.info("STAGE <<<<<<<<<<<< Initializing the Data Tranformation Config >>>>>>>>>>>>")
    data_tansformation_config=DataTransformationConfig(training_pipeline_config)
    logger.info("STAGE <<<<<<<<<<<< Initialized the Data Transformation Config Successfully >>>>>>>>>>>>")

    logger.info("STAGE <<<<<<<<<<<< Initiating Data Transformation Pipeline >>>>>>>>>>>>")
    data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,
                                           data_transformation_config=data_tansformation_config)
    
    logger.info("STAGE <<<<<<<<<<<< Initiating the data transformation and collecting transformed data and object >>>>>>>>>>>>")
    data_transformation_artifact=data_transformation.initiate_data_transformation()
    print(data_transformation_artifact)
    logger.info("STAGE <<<<<<<<<<<< Data Transformation Completed >>>>>>>>>>>>")


    ################################## Model Trainer ##################################

    logger.info("STAGE <<<<<<<<<<<< Initializing the Model Config >>>>>>>>>>>>")
    model_trainer_config=ModelTrainerConfig(training_pipeline_config)
    logger.info("STAGE <<<<<<<<<<<< Initialized the Model Trainer Config Successfully >>>>>>>>>>>>")

    logger.info("STAGE <<<<<<<<<<<< Initiating Data Transformation Pipeline >>>>>>>>>>>>")
    model_trainer=ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                           model_trainer_config=model_trainer_config)
    
    logger.info("STAGE <<<<<<<<<<<< Initiating the data transformation and collecting transformed data and object >>>>>>>>>>>>")
    model_trainer_artifact=model_trainer.initiate_model_training()
    print(model_trainer_artifact)
    logger.info("STAGE <<<<<<<<<<<< Data Transformation Completed >>>>>>>>>>>>")