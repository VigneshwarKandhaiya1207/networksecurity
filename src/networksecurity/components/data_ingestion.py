import os
import sys
import pandas as pd
import pymongo
import numpy as np
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from src.networksecurity.logger.logger import logger
from src.networksecurity.utils.utils import create_directories
from src.networksecurity.exception.exception import NetworkSecurityException
from src.networksecurity.entity.config_entity import DataIngestionConfig
from src.networksecurity.entity.artifact_entity import DataIngestionArtifact


load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        self.data_ingestion_config=data_ingestion_config

    def export_collection_as_dataframe(self):
        logger.info("Initiating the data ingestion from Mongo DB.")
        try:
            self.database_name=self.data_ingestion_config.database_name
            self.collection_name=self.data_ingestion_config.collection_name
            logger.info("Database name : {}".format(self.database_name))
            logger.info("Collection name : {}".format(self.collection_name))
            self.client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.client[self.database_name][self.collection_name]

            data=pd.DataFrame(list(collection.find()))
            logger.info("Check for _id in the dataframe columns.")
            if "_id" in data.columns.to_list():
                logger.info("Found the column '_id'. Dropping the column ")
                data=data.drop(columns=["_id"],axis=1)
                logger.info("Dropped the column '_id'.")
            
            data.replace({"na":np.nan},inplace=True)
            return data
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_into_featurestore(self,dataframe:pd.DataFrame):
        feature_store_file_path=self.data_ingestion_config.feature_store_file_path
        try:
            create_directories([os.path.dirname(feature_store_file_path)])
            logger.info("Exporting the raw data to local file path {}".format(feature_store_file_path))
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            logger.info("Exported the documents as CSV {}".format(feature_store_file_path))
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            logger.info("Initiating the train test split with {} as test size".format(self.data_ingestion_config.train_test_split_ratio))
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)
            logger.info("Data split completed successfully")
            create_directories([os.path.dirname(self.data_ingestion_config.training_file_path)])
            logger.info("Exporting the train data to {}".format(self.data_ingestion_config.training_file_path))
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False, header=True)
            logger.info("Train data exported successfully")
            create_directories([os.path.dirname(self.data_ingestion_config.test_file_path)])
            logger.info("Exporting the test data to {}".format(self.data_ingestion_config.test_file_path))
            test_set.to_csv(self.data_ingestion_config.test_file_path)
            logger.info("Test data exported successfully")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def initiate_data_ingestion(self):
        try:
            data=self.export_collection_as_dataframe()
            data=self.export_data_into_featurestore(data)
            self.split_data_as_train_test(data)
            data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.test_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        