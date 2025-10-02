#!/bin/bash

# set e

SERVER_SSH=$1
DEPLOY_PATH=$2
SSH_KEY=$3
DOCKER_REPOSITORY=$4
DEPLOY_ENV=$5


ROOT_DIR=$(git rev-parse --show-toplevel)
cd ${ROOT_DIR}

#syn source to deploy server
echo syn source to server
rsync -e "ssh -i ${SSH_KEY}" -avzh --delete-after --omit-dir-times --exclude '.git' ./  ${SERVER_SSH}:${DEPLOY_PATH}
cd ${SOURCE_DIR}

#build and run docker container
echo building source...
ssh -i ${SSH_KEY} ${SERVER_SSH} env DEPLOY_PATH="$DEPLOY_PATH" DOCKER_REPOSITORY="$DOCKER_REPOSITORY" DEPLOY_ENV="$DEPLOY_ENV"  /bin/bash <<'EOT'
cd ${DEPLOY_PATH}
echo run docker container
docker-compose up -d --build
echo deploying finished. || exit 1\
EOT
