import os, subprocess, argparse, json
from os.path import dirname, join
import traceback
import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup


class BuildStatus:
    # open > scheduling > in_progress > processed > deployed or failed
    OPEN = 0
    SCHEDULING = 1
    IN_PROGRESS = 2
    PROCESSED = 3
    DEPLOYED = 4
    FAILED = 5

BASE_DIR = dirname(__file__)
print (f"BASE_DIR: {BASE_DIR}")

def parse_input_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', type=str, help="build id", required=True)
    parser.add_argument('--backend', type=str, help="backend url", default=None)
    parser.add_argument('--username', type=str, help="admin username", default=None)
    parser.add_argument('--password', type=str, help="admin password", default=None)
    parser.add_argument('--auth', type=str, help="auth token", default=None)
    args = parser.parse_args()
    build_id = args.build
    buidl_backend_url = None
    build_username = None
    build_password = None
    auth_token = None
    if args.backend is not None:
        buidl_backend_url = args.backend
    if args.username is not None:
        build_username = args.username
    if args.password is not None:
        build_password = args.password
    if args.auth is not None:
        auth_token = args.auth
    return build_id, buidl_backend_url, build_username, build_password, auth_token


def get_auth(backend_url, username, password):
    try:
        if backend_url is not None and backend_url != "" and password is not None and password != "":
            url = f"{backend_url}/api/v1/employees/login"
            payload = { "username": username, "password": password }
            response = requests.post(url=url, data=payload)
            response.raise_for_status() ## raise exception if response code is not 200
            auth = response.json()
            auth_token = " ".join([auth["token_type"], auth["access_token"]])
        if auth_token == "":
            auth_token =  None
        return auth_token
    except Exception as error:
        print('pipeline failed to authenticate:')
        print(error)
        return None

def log_error(error, build_id, backend_url, auth_token, traceback=None):
    url = f"{backend_url}/api/v1/websites/builds/{build_id}"
    headers = { 
        "Authorization": auth_token,
        # 'Content-Type': 'multipart/form-data', 
    }
    info = { "log": f"{error}" }
    if traceback is not None:
        info.update({ "traceback": traceback })
    payload = {
        "info": json.dumps(info),
        "status": BuildStatus.FAILED
    }
    response = requests.put(url=url, headers=headers, data=payload)
    print(response.text)

def get_site_info(build_id, backend_url, token):
    headers = { "Authorization": token }
    site_id = None
    ## Get build info
    try:
        url = f"{backend_url}/api/v1/websites/builds/{build_id}"
        payload = {
            "info": json.dumps({ "log": "In progress..." }),
            "status": BuildStatus.IN_PROGRESS
        }
        response = requests.put(url=url, headers=headers, data=payload)
        response.raise_for_status() ## raise exception if response code is not 200
        # print(response.text)
        result = json.loads(response.text)
        site_id = result["site_id"]
    except Exception as error:
        traceback_string = traceback.format_exc()
        print('get_build_info exception:')
        print(traceback_string)
        return None
    ## Get site info
    if site_id is None:
        return  None
    
    try:
        url = f"{backend_url}/api/v1/websites/sites/{site_id}"
        response = requests.get(url=url, headers=headers)
        response.raise_for_status() ## raise exception if response code is not 200
        return json.loads(response.text)
    except Exception:
        traceback_string = traceback.format_exc()
        print('get_site_info exception:')
        print(traceback_string)
        return None


def download_template(site, build_id):
    try:
        url = site["template"]
        if url is None:
            return
        response = requests.get(url=url)
        response.raise_for_status() ## raise exception if response code is not 200
        template_zip_path = join(BASE_DIR, "builds", build_id, "template.zip")
        with open(template_zip_path, "wb") as output:
            output.write(response.content)
        ## unzip template
        template_unzip_path = join(BASE_DIR, "builds", build_id, "template")
        with ZipFile(template_zip_path) as zip:
            zip.extractall(path=template_unzip_path)
        return template_unzip_path
    except Exception as error:
        traceback_string = traceback.format_exc()
        print('download_template exception:')
        print(traceback_string)
        raise error

def apply_build_config(site, template_dir):
    #Todo: implement this method to preprocess nuxt config file, tailwind conffig file and element-plus config file.
    pass

def build_website(site, template_dir, build_id):
    try:
        siteId = site.get("id")
        ## build subprocess
        site_info_file_path = join(BASE_DIR, "builds",  build_id, "site.json")
        with open(site_info_file_path, "w", encoding='utf8') as output:
            output.write(json.dumps(site))
        exist = os.path.isdir(template_dir)
        info_exist = os.path.isfile(site_info_file_path)
        print(f"{template_dir} exist: {exist}")
        print(f"{site_info_file_path} exist: {info_exist}")
        command = f"cd {template_dir} && npm install && npm run prepare-package {site_info_file_path}"
        subprocess.run(command, shell=True)
        ## collect build output & zip it
        build_output_dir = join(template_dir, '.nuxt', 'dist')
        output_zip_path = join(BASE_DIR, "builds", build_id, f"{siteId}.zip")
        with ZipFile(output_zip_path, "w") as zip:
            for path, folders, files in os.walk(build_output_dir):
                ## copy all file in .output folder
                for filename in files:
                    filepath = os.path.join(path, filename)
                    arcname = os.path.relpath(filepath, build_output_dir)
                    zip.write(filepath, arcname=arcname)
                    ## rename client.manifest files & copy to client.manifest folder
                    if "client.manifest" in filename:
                        filename = filename.replace("client", siteId)
                        arcname = os.path.join("client.manifest", filename)
                        zip.write(filepath, arcname=arcname)
            return output_zip_path
    except Exception as error:
        traceback_string = traceback.format_exc()
        print(traceback_string)
        print('build_website exception:')
        raise error

def audit_html(html_path, build_id, site_id):
    """audit html file to django-template-lang format

    :param html_file: path to html file
    """
    try:
        with open(html_path, 'r', encoding='utf8') as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        ## remove <script type="module">
        soup.find(type='module').replace_with("")
        ## insert django template tag
        soup.html.insert_before("{% load static %}\n{% load i18n %}\n{% load django_vite %}\n")
        ## edit <head>
        style = soup.style.replace_with("")
        title = soup.new_tag('title', string=r"{{ title }}")
        meta = soup.new_tag('meta', attrs={"name":r"{{ item.name }}", "content":r"{{ item.content }}"})
        head = soup.head
        head.extend([
            "{% for item in metadata %}",
            meta,
            "{% endfor %}",
            title,
            style,
            "{% vite_asset 'node_modules/nuxt/dist/app/entry.js' app='"+site_id+"' %}",
        ])
        ## edit app.buildAssetsDir, etc...
        new_config_app = {
            "baseURL": "/",
            "buildId": f"{build_id}",
            "buildAssetsDir": f"{site_id}/public/_nuxt/",
            "cdnURL": ""
        }
        script = soup.body.find_all('script')[-1]
        start = script.string.find('app')
        end = script.string.find('}', start)
        config_app = script.string[start:end+1]
        script.string = script.string.replace(config_app, "app:"+str(new_config_app))
        ## write output
        with open(html_path, 'w', encoding='utf8') as f:
            f.write(soup.prettify())
    except Exception as error:
        print('audit_html exception:')
        raise error


def generate_html(site, template_dir, build_id):
    try:
        siteId = site.get("id")
        ## generate subprocess
        command = f"cd {template_dir} && npm i && npm run create-template-preview"
        subprocess.run(command, shell=True)
        ## add html output to zip
        build_output_dir = os.path.join(template_dir, '.output')
        output_zip_path = join(BASE_DIR, "builds", build_id, f"{siteId}.zip")
        with ZipFile(output_zip_path, "a") as zip:
            for path, folders, files in os.walk(build_output_dir):
                for filename in files:
                    filepath = join(path, filename)
                    if "preview.html" in filename:
                        audit_html(filepath, build_id, siteId)
                        zip.write(filepath, arcname=f"{siteId}.html")
        return output_zip_path
    except Exception as error:
        traceback_string = traceback.format_exc()
        print('generate_html exception:')
        print(traceback_string)
        raise error
    

def upload_build(site, build_id, build_backend_url, auth_token):
    try:
        siteId = site.get("id")
        output_zip_path = join(BASE_DIR, "builds", build_id, f"{siteId}.zip")
        with open(output_zip_path,'rb') as zip:
            url = f"{build_backend_url}/api/v1/websites/builds/{build_id}"
            headers = { 
                "Authorization": auth_token,
                # 'Content-Type': 'multipart/form-data', 
            }
            payload = {
                "info": json.dumps({ "log": "Build uploaded" }),
                "status": BuildStatus.PROCESSED
            }
            files = [
                ('archive', (f"{build_id}.zip", zip, 'application/zip'))
            ]
            response = requests.put(url=url, headers=headers, data=payload, files=files)
            response.raise_for_status()
            # print(response.text)
            result = json.loads(response.text)
            print(f"Uploaded, site_id={result["site_id"]}, build_id={result["id"]}")
    except Exception as error:
        traceback_string = traceback.format_exc()
        print('upload_build exception:')
        print(traceback_string)
        raise error


def deploy(build_id, build_backend_url, auth_tokem):
    try:
        url = f"{build_backend_url}/api/v1/websites/builds/{build_id}/deploy"
        headers = { 
            "Authorization": auth_tokem,
        }
        response = requests.post(url=url, headers=headers)
        response.raise_for_status()
    except Exception as error:
        traceback_string = traceback.format_exc()
        print('deploy exception:')
        print(traceback_string)
        raise error


## main
print("parse params")
build_id, buidl_backend_url, build_username, build_password, auth_token = parse_input_params()
try:
    print("Authorizing...")
    if auth_token is None or auth_token == "":
        auth_token = get_auth(buidl_backend_url, build_username, build_password)
    if auth_token:
        print("Geting site information")
        site = get_site_info(build_id, buidl_backend_url, auth_token)
        if site is not None:
            print("Downloading template...")
            unzip_path = download_template(site, build_id)
            if unzip_path is not None:
                print("Appling config...")
                apply_build_config(site, unzip_path)
                print("Building javascript and css...")
                build_website(site, unzip_path, build_id)
                print("Generating html...")
                generate_html(site, unzip_path, build_id)
                print("Uploading build...")
                upload_build(site, build_id, buidl_backend_url, auth_token)
                print("Deploing...")
                deploy(build_id, buidl_backend_url, auth_token)
except Exception as error:
    traceback_string = traceback.format_exc()
    if build_id is not None and buidl_backend_url is not None and auth_token is not None:
        log_error(error, build_id, buidl_backend_url, auth_token, traceback_string)
    raise error