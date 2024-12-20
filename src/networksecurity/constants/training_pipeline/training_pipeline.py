import os
import sys
import numpy as np

"""
defining the common constant variables for the training pipeline
"""

TARGET_COLUMN:str="Result"
PIPELINE_NAME: str="NetworkSecurity"
ARTIFACTS_DIR: str="Artifacts"
FILE_NAME: str="phisingData.csv"
TRAIN_FILE_NAME: str="train.csv"
TEST_FILE_NAME: str="test.csv"

SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")
SAVED_MODEL_DIR =os.path.join("saved_models")
FINAL_MODEL_DIR=os.path.join("final_model")
MODEL_FILE_NAME = "model.pkl"

"""
Dataingestion related constant start with DATA_INGESTION VAR NAME 
"""

DATA_INGESTION_DATABASE_NAME: str="networksecurity"
DATA_INGESTION_COLLECTION_NAME: str="phisingdata"
DATA_INGESTION_DIR_NAME: str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str="feature_store"
DATA_INGESTION_INGESTED_DIR: str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float=0.2

"""
DataValidation related constant start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME: str="data_validation"
DATA_VALIDATION_VALID_DIR: str="validated"
DATA_VALIDATION_INVALID_DIR: str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str="report.yaml"

"""
DataTransformation related constant starts with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME:str="data_tansformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str="transformed"
DATA_TANSFORMATION_TRANSFORMED_OBJECT_DIR:str="transformed_object"
PREPROCESSING_OBJECT_FILE_NAME:str="preprocesser.pkl"
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"

DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"

"""
Model Trainer related constants starts with MODEL_TRAINER VAR NAME
"""

MODEL_TRAINER_DIR_NAME:str="model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str="trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str="model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float=0.6
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD: float = 0.05

BUCKET_NAME="network-security-artifacts-model"
S3_BUCKET_ARTIFACTS_DIR="artifacts"
S3_BUCKET_MODEL_DIR="models"