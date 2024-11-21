import os
import sys
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from src.networksecurity.logger.logger import logger
from src.networksecurity.exception.exception import NetworkSecurityException
from src.networksecurity.constants.training_pipeline.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS,PREPROCESSING_OBJECT_FILE_NAME
from src.networksecurity.entity.config_entity import DataTransformationConfig
from src.networksecurity.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from src.networksecurity.utils.utils import read_yaml,create_directories,save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):

        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        return pd.read_csv(file_path)
    
    def get_preprocessor_object(cls):
        try:
            logger.info("Creating the preprocessor object")
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor=Pipeline(steps=[
                ("imputer",imputer)
            ])
            return preprocessor
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
    def initiate_data_transformation(self)-> DataTransformationArtifact:
        try:
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)


            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)

            logger.info("Getting the preprocessor object")
            preprocessor=self.get_preprocessor_object()
            logger.info("Preprocessor object successfully assigned.")

            logger.info("Fit using the preprocessor objects")
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            #preprocessor_object=preprocessor.fit(input_feature_train_df)
            logger.info("Fit successful.")

            transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor_object.transform(input_feature_test_df)

            train_array=np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_array=np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_array)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_array)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)
            save_object(os.path.join(self.data_transformation_config.final_model_dir,PREPROCESSING_OBJECT_FILE_NAME),preprocessor_object)


            data_transformation_artifact=DataTransformationArtifact(transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path)
            
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

        
