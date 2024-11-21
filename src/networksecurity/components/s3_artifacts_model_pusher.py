import os
import sys
import boto3
import subprocess
from dotenv import load_dotenv

load_dotenv()

class S3Client:

    def push_to_s3(self,local_directory,bucket_path):
        command_to_run=f"aws s3 sync {local_directory} {bucket_path}"
        subprocess.run(command_to_run,shell=True)
        

    def pull_from_s3(self,bucket_path,local_directory):
        command_to_run=f"aws s3 sync {bucket_path} {local_directory}"
        subprocess.run(command_to_run,shell=True)