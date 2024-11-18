import os
import sys
from pathlib import Path

project_name="networksecurity"

list_of_files=[
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    "main.py",
    "Dockerfile",
    "setup.py"
]

for file_path in list_of_files:
    file_path=Path(file_path)
    file_dir,file_name=os.path.split(file_path)

    if file_dir!="":
        try:
            os.makedirs(file_dir,exist_ok=True)
            print("Created the directory {}".format(file_dir))
        except Exception as e:
            print("Directory creation failed with error {}".format(e))
        
    if (not os.path.exists(file_path)) or (os.path.getsize==0):
        with open(file_path,"w") as f:
            pass
