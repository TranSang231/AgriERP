import os, subprocess, json
import sys
from os.path import dirname, join
import requests
from shutil import rmtree
from dotenv import dotenv_values


## Params
BUILD_BACKEND_URL = "http://127.0.0.1:8008"
BUILD_USERNAME = ""
BUILD_PASSWORD = ""

## Var
AUTH_TOKEN = ""
BUILDS = []

class BuildStatus:
    # open > scheduling > in_progress > processed > deployed or failed
    OPEN = 0
    SCHEDULING = 1
    IN_PROGRESS = 2
    PROCESSED = 3
    DEPLOYED = 4
    FAILED = 5

## Config
BASE_DIR = dirname(dirname(__file__))


def get_env():
    global BUILD_BACKEND_URL, BUILD_USERNAME, BUILD_PASSWORD
    env = dotenv_values(os.path.join(BASE_DIR, '.env'))
    BUILD_BACKEND_URL = (
        os.environ["BUILD_BACKEND_URL"]
        if "BUILD_BACKEND_URL" in os.environ
        else env.get("BUILD_BACKEND_URL", "http://127.0.0.1:8008")
    )
    BUILD_USERNAME = (
        os.environ["BUILD_USERNAME"]
        if "BUILD_USERNAME" in os.environ
        else env.get("BUILD_USERNAME", "")
    )
    BUILD_PASSWORD = (
        os.environ["BUILD_PASSWORD"]
        if "BUILD_PASSWORD" in os.environ
        else env.get("BUILD_PASSWORD", "")
    )


def get_auth():
    global AUTH_TOKEN
    try:
        if (BUILD_USERNAME!="" and BUILD_PASSWORD!=""):
            url = f"{BUILD_BACKEND_URL}/api/v1/employees/login"
            payload = { "username": BUILD_USERNAME, "password": BUILD_PASSWORD }
            response = requests.post(url=url, data=payload)
            response.raise_for_status()
            auth = response.json()
            AUTH_TOKEN = " ".join([auth["token_type"], auth["access_token"]])
        if AUTH_TOKEN=="":
            print("Can't get auth token")
            raise Exception("Can't get auth token")
    except Exception as error:
        print('get_auth exception:')
        raise error


def get_open_builds():
    global BUILDS
    try:
        url = f"{BUILD_BACKEND_URL}/api/v1/websites/builds?status={BuildStatus.OPEN}"
        headers = { "Authorization": AUTH_TOKEN }
        response = requests.get(url=url, headers=headers)
        response.raise_for_status() ## raise exception if response code is not 200
        result = json.loads(response.text)
        
        if len(result) > 0:
            BUILDS = [build["id"] for build in result]
            print('Scheduling builds:', BUILDS)
        else:
            print('There are no build to handle at the moment.')
    except Exception as error:
        print('Could not fetch build:')
        raise error
    

def start_build():
    try:
        if len(BUILDS) > 0:
            build_pipelines = []
            ## start subprocess for each build_id
            for build_id in BUILDS:
                build_folder = join(BASE_DIR, "builds", build_id)
                template_folder = join(build_folder, "template")
                if not os.path.exists(template_folder):
                    os.makedirs(template_folder, exist_ok=True)
                    print(f"folder created: {template_folder}")
                exist = os.path.isdir(template_folder)
                print(f"{template_folder} exist: {exist}")
                command = f"python {BASE_DIR}/build-pipeline.py --build={build_id} --backend={BUILD_BACKEND_URL} --auth=\"{AUTH_TOKEN}\""
                process = subprocess.Popen(command, shell=True)
                build_pipelines.append((build_id, build_folder, process))
            ## wait for all subprocess to finish, then clean up
            for (build_id, build_folder, process) in build_pipelines:
                process.wait()
                print("Build pipeline for build_id", build_id, "return with code", process.returncode)
                ## clean up build folder
                # rmtree(build_folder)
    except Exception as error:
        print('start_build exception:')
        print(error)
        raise error


## main
try:
    print('Running schedule build job...')
    get_env()
    get_auth()
    get_open_builds()
    start_build()
except Exception as error:
    print('Exception raised when running, skipping this time. Exception detail:')
    raise error