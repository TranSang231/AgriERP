FROM python:3.12-slim

## Create a group and user to run our app
ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

## install utils
RUN apt-get update && apt-get -y install cron xz-utils curl

## use python3
RUN ln -s /usr/bin/python3 /usr/bin/python & \
    ln -s /usr/bin/pip3 /usr/bin/pip

## install node:22.14.0
RUN curl https://nodejs.org/dist/v22.14.0/node-v22.14.0-linux-x64.tar.xz -O
RUN tar -xf node-v22.14.0-linux-x64.tar.xz
RUN ln -s /node-v22.14.0-linux-x64/bin/node /usr/local/bin/node
RUN ln -s /node-v22.14.0-linux-x64/bin/npm /usr/local/bin/npm
RUN ln -s /node-v22.14.0-linux-x64/bin/npx /usr/local/bin/npx

## copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /code/
WORKDIR /code/
COPY ./.env ./
COPY ./requirements.txt ./
COPY ./build-pipeline.py ./
COPY ./schedule.py ./
COPY ./crontab /etc/cron.d/crontab

## install requirements
RUN python -m pip install -r requirements.txt

# cron: add job
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab


CMD ["cron", "-f"]

## From docker cli:
## `docker build -t build-website -f Dockerfile.template .`
## `docker run --name build-container build-website`