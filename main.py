import os
import sys
from src.networksecurity.logger.logger import logger
from src.networksecurity.exception.exception import NetworkSecurityException
from src.networksecurity.pipeline.train_pipeline import TrainingPipeline

if __name__=="__main__":
    
    training_pipeline=TrainingPipeline()
    training_pipeline.run_pipeline()

