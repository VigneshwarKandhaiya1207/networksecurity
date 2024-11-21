import os
import sys
from src.networksecurity.logger.logger import logger
from src.networksecurity.exception.exception import NetworkSecurityException
from src.networksecurity.constants.training_pipeline.training_pipeline import BUCKET_NAME,S3_BUCKET_ARTIFACTS_DIR,S3_BUCKET_MODEL_DIR
from src.networksecurity.components.s3_artifacts_model_pusher import S3Client
from src.networksecurity.entity.config_entity import (TrainingPipelineConfig,DataIngestionConfig,DataTransformationConfig,
                                                      DataValidationConfig,ModelTrainerConfig)
from src.networksecurity.entity.artifact_entity import (DataIngestionArtifact,DataValidationArtifact,
                                                        DataTransformationArtifact,ModelTrainerArtifact)
from src.networksecurity.components.data_ingestion import DataIngestion
from src.networksecurity.components.data_validation import DataValidation
from src.networksecurity.components.data_transformation import DataTransformation
from src.networksecurity.components.model_trainer import ModelTrainer

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
        self.s3_sync=S3Client()
    
    def start_data_ingestion(self):
        try:
            logger.info("Initiating Data Ingestion Pipeline")
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            self.data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            self.data_ingestion_artifact=self.data_ingestion.initiate_data_ingestion()
            logger.info("Data Ingestion pipeline completed")
            return self.data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            logger.info("Initiating Data Validation Pipeline")
            self.data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            self.data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                                data_validation_config=self.data_validation_config)
            self.data_validation_artifact=self.data_validation.initiate_data_validation()
            logger.info("Data Validation pipeline completed")
            return self.data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            logger.info("Initiating Data Transformation pipeline")
            self.data_transformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            self.data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,
                                                        data_transformation_config=self.data_transformation_config)
            self.data_transformation_artifact=self.data_transformation.initiate_data_transformation()
            return self.data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            logger.info("Initiating Model Training")
            self.model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            self.model_trainer=ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                            model_trainer_config=self.model_trainer_config)
            self.model_trainer_artifact=self.model_trainer.initiate_model_training()
            return self.model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{BUCKET_NAME}/{S3_BUCKET_ARTIFACTS_DIR}/{self.training_pipeline_config.timestamp}"
            self.s3_sync.push_to_s3(local_directory = self.training_pipeline_config.artifact_dir,bucket_path=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    ## local final model is going to s3 bucket 
        
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{BUCKET_NAME}/{S3_BUCKET_MODEL_DIR}/{self.training_pipeline_config.timestamp}"
            self.s3_sync.push_to_s3(local_directory = self.training_pipeline_config.model_dir,bucket_path=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
