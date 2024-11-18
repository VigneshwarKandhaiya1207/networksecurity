import os
import sys
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
from src.networksecurity.logger.logger import logger
from src.networksecurity.constants.training_pipeline.training_pipeline import SCHEMA_FILE_PATH
from src.networksecurity.utils.utils import create_directories,read_yaml,write_yaml
from src.networksecurity.exception.exception import NetworkSecurityException
from src.networksecurity.entity.config_entity import DataValidationConfig
from src.networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact


class DataValidation:
    def __init__(self,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return(pd.read_csv(file_path))
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def validate_columns(self,dataframe: pd.DataFrame)-> bool:
        try:
            validation_check=True
            keys_list = [key for cols in self._schema_config['columns'] for key in cols.keys()]
            base_schema_column_count=len(keys_list)
            current_schema_column_count=len(dataframe.columns.to_list())
            
            if (base_schema_column_count == current_schema_column_count):
                for cols in dataframe.columns.to_list():
                    if cols not in (keys_list):
                        validation_check=False
                        return validation_check
                                                
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        return validation_check


    def detect_dataset_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns.to_list():
                d1=base_df[column]
                d2=current_df[column]
                is_same_distribution=ks_2samp(d1,d2)
                if threshold<=is_same_distribution.pvalue:
                    is_drift_found=False
                else:
                    is_drift_found=True
                    status=True
                report.update({column:{
                    "p_value":float(is_same_distribution.pvalue),
                    "drift_status":is_drift_found
                    
                    }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            create_directories([dir_path])
            write_yaml(file_path=drift_report_file_path,content=report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def initiate_data_validation(self):
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            best_train_file_path=self.data_ingestion_artifact.trained_file_path
            best_test_file_path=self.data_ingestion_artifact.test_file_path

            train_data_frame=DataValidation.read_data(train_file_path)
            test_data_frame=DataValidation.read_data(test_file_path)

            best_train_data_frame=DataValidation.read_data(best_train_file_path)
            best_test_data_frame=DataValidation.read_data(best_test_file_path)

            train_col_validation=self.validate_columns(train_data_frame)
            test_col_validation=self.validate_columns(test_data_frame)
            
            self.detect_dataset_drift(base_df=best_train_data_frame,current_df=train_data_frame)

            if not train_col_validation or not test_col_validation:
                logger.info("The schema validation failed.")
                logger.info("Train Columns Validation : {}".format(train_col_validation))
                logger.info("Test Columns Validation : {}".format(test_col_validation))         
                logger.info("Writing the invalid data to {}".format(os.path.dirname(self.data_validation_config.invalid_train_file_path)))      
                dir_path=os.path.dirname(self.data_validation_config.invalid_train_file_path)
                create_directories([dir_path])
                logger.info("Invalid Train path : {}".format(self.data_validation_config.invalid_train_file_path))
                train_data_frame.to_csv(self.data_validation_config.invalid_train_file_path)
                logger.info("Invalid Test Path : {}".format(self.data_validation_config.invalid_test_file_path))
                test_data_frame.to_csv(self.data_validation_config.invalid_test_file_path)
            else:
                logger.info("The schema validation Succeeded.")
                logger.info("Train Columns Validation : {}".format(train_col_validation))
                logger.info("Test Columns Validation : {}".format(test_col_validation))         
                logger.info("Writing the Valid data to {}".format(os.path.dirname(self.data_validation_config.valid_train_file_path)))      
                dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
                create_directories([dir_path])
                logger.info("Invalid Train path : {}".format(self.data_validation_config.valid_train_file_path))
                train_data_frame.to_csv(self.data_validation_config.valid_train_file_path)
                logger.info("Invalid Test Path : {}".format(self.data_validation_config.valid_test_file_path))
                test_data_frame.to_csv(self.data_validation_config.valid_test_file_path)


            data_validation_artifact = DataValidationArtifact(
                validation_status=train_col_validation,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        


