# ML_Project
Project Demo. for End to End ML Project

1. GitHub Repo.
2. Cloned Git Hub repo in Local PC
3. open command prompt : got clone https:git......
4. Locad folde in VSCode

5. Created CONDA environment using Command prompt
command : conda create -p new venv python==3.7 -y


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
    