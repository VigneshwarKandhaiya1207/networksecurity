import os
from setuptools import setup,find_packages
from typing import List

def get_requirement()-> List[str]:
    requirements_lst:List[str]=[]
    try:
        if os.path.exists("requirements.txt"):
            with open("requirements.txt","r") as file_handler:
                files=file_handler.readlines()
                
                for file in files:
                    requirement=file.strip()
                    if requirement and requirement!="-e .":
                        requirements_lst.append(requirement)
        else:
            print("File : requirements.txt not found.")
    except Exception as e:
        print("Failed with exception {}".format(e))
    
    return requirements_lst

setup(
    name="networkSecurity",
    author="Vigneshwar Kandhaiya",
    author_email='vigneshwar.k2@gmail.com',
    version="0.0.1",
    packages=find_packages(),
    install_requires=get_requirement()
)