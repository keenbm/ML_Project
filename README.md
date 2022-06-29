# ML_Project
Project Demo. for End to End ML Project

1. GitHub Repo.
2. Cloned Git Hub repo in Local PC
3. open command prompt : got clone https:git......
4. Locad folde in VSCode

5. Created CONDA environment using Command prompt
command : conda create -p venv python==3.7 -y


-p : Creats python environment in project folder it self.
-y : it automatically accept warning after executing command
If we dont write -p then Vir. Env will be created in Anconda3 directory

6. Activate virtual environment using Command prompt
command : conda activate venv/

7. Create requirement.txt file

8. Install requirements in virtual env:
pip install -r requirements.txt

9. Add ENV folder in .gitignore
so that ENV folde will not be sent to github

10. git status (if files are changed and not commited then it'll will show red color text)
                (If files are not changed or commited then it'll show green color text)
    git add xxx (xxx = file name) (add specific file for commit)
    git add .   (add files for commit)
    git log (gives all version/commits history)
    git commit -m "message" (Creates new version in local system)
    git push origin main (Push version/change to GitHub) main = Branch name
    git remote -v (check remote url)
    git revert -- (for editing rolling back commit)

11. Setup CI/CD pipeline
    Info. required from Heroku
    1. HEROKU_EMAIL = bmodi700@gmail.com
    2. HEROKU_API_KEY= ----
    3. HEROKU_APP_NAME= ml-regression-demo-app

 12. For docker (to create docker image locally) (Not required for Heroku deployment) :
    Create file named "Dockerfile" and ".dockerignore" and add following :
    Dockerfile :
     - Write operating system

    .dockerignore : (mentioned file/folder =s to be ignored for docker):
    i.e. /venv, .git , .gitignore

    BUILD DOCKER IMAGE
    Command : docker build -t <image_name>:<tag_name>

    List docker images :
    Command : docker images

    Run docker image :
    Command : docker -run -p 5000:5000 -e PORT=5000 <image-id>

    To Check running container in docker :
    Command : docker ps


    To Stop docker container
    Command : docker stop <container_id>

13. For Heroku Deployment :
    Create Folder : .github\workflow
    Under this file Create : main.yaml

    YAML file create workflow and Create GitHub action and trigger.

 14. This file content we can get it from internet and update following :
    
    Create sercrets in Github for following : 
    EMAIL
    API KEY
    APP NAME

15. Got to Action in GitHub run BUILD.
    It'll deploy app to Heroku16. So when every time when we commit and Push new code to Github
    Github action will be triggered and New code will be deployed to Heroku

16. Create Housing Folder
    - Under Housing create __init__
   
17. Create setyp.py and Project related content
   - after writing setup.py
     python setup.py install or (pip install -r requirements.txt)
     refer setup.py file comments for more details

18. After initial setup , working folder will be "housing"

Housing
|-__init__.py
|-Exception package
|  |
|  |-__init__.py
|
|-Logger package
|  |
|  |-__init__.py
|
|-pipeline package
|  |
|  |-__init__.py
|
|-component package
|  |
|  |-__init__.py
|
|-config package
|  |
|  |-__init__.py
|
|-entity package
|  |
|  |-__init__.py
|
|- util
|   |
|   |-__init__.py
|   |- util.py  ## for utility function i.e. read yaml
|
|- constant
|   |
|   |-__init__.py
|   |- constant.py ## Store constant i.e. file path etc.
|_________________

19. First create code for Logger module

20. Created Code for Exception module

21. Created Configuration = entity --> config_entity.py and artificat_entity.py
    In this file datastructure are created for logging
    all type configuration  
    dataIngestion , datavalidation , datatransformation , train moel , evaluatio data
    are mentioned

22. Creating Config folder in main directory
   - Create config.yml file for pipe creation
   - Basically this file stores file path and Variables name related to pipeline
   - So we only need to change this file for changing piple line parameter

23. Create : Housing folder > Config folder > Config.python
    - In this file class and function are written to 
      get values/path from configuration files (config.yml)
    -  We are using following in this python file :
       Importing Constant.py
       Reading config.yml
       Importing config_entity.py and assigning values to it's datastructure (named tuple) after reading it from config.yml

24. Creating and coding component > data_ingestion.py

25. Create Pipeline > Pipeline.py





   Ref : https://github.com/avnyadav/machine_learning_project/tree/main/housing/entity