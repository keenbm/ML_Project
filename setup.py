from setuptools import find_packages, setup
from typing import List

#Declaring variables for setup functions
PROJECT_NAME="housing-predictor"
VERSION="0.0.1"
AUTHOR="Bhavik Modi"
DESRCIPTION="End to End Projet for CI/CD and diff. ML algo demo."
PACKAGES=["housing"]
REQUIREMENT_FILE_NAME="requirements.txt"


def get_requirements_list()->List[str]:
    """
    Description: This function is going to return list of requirement
    mention in requirements.txt file
    return This function is going to return a list which contain name
    of libraries mentioned in requirements.txt file
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        return requirement_file.readlines().remove("-e.")


setup(
name=PROJECT_NAME,
version=VERSION,
author=AUTHOR,
description=DESRCIPTION,
packages=find_packages(),
install_requires=get_requirements_list() 
)


## install_requires -->>
#  Get and install external library (numpy,python etc etc)  from requirement.txt

## packages=find_packages()-->>
#  get folders/package which cointains __init__.py file
# (to install internal custom packages i.e. housing-predictor v.0.0.1)


## -e. ->> This will install internal custom packages (i.e. housing-predictor v.0.0.1 )

## pip install -e. AND packages=find_packages() DO SAME TASK
## if requirement.txt is directly installed (by bypassing setup.py)
# then -e. , should be present in requirement.txt file
# If we do project setup by running "python setup.py install" then we need to removr "-e."" using
#  "requirement_file.readlines().remove("-e.")" in install_requires parameter. This will ensure that
# we are not installing internal custom packages 2 times

## setup.py or requirements.txt with ".e-"
# installation automatically creats xxx.egg-info folder