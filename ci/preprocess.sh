#!/bin/bash

set -e

ROOT_DIR=$(git rev-parse --show-toplevel)
BACKEND_DIR=${ROOT_DIR}/backend
cd ${ROOT_DIR}

# Copy or download scret files
scp -i ${SSH_KEY} ${SERVER_SSH}:${CLIENT_SECRET_FILE} ${BACKEND_DIR}/firebase/credentials/serviceAccountKey.json

# For docker
echo preprocess docker environment variables
cp -f ${ROOT_DIR}/ci/docker.env.template ${ROOT_DIR}/docker.env
find ${ROOT_DIR}/docker.env -type f -name "*" | xargs sed -i'' s/DJANGO_SETTINGS_MODULE=/DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}/g
find ${ROOT_DIR}/docker.env -type f -name "*" | xargs sed -i'' s/DB_HOST=/DB_HOST=${DB_HOST}/g
find ${ROOT_DIR}/docker.env -type f -name "*" | xargs sed -i'' s/DB_PORT=/DB_PORT=${DB_PORT}/g
find ${ROOT_DIR}/docker.env -type f -name "*" | xargs sed -i'' s/DB_USER=/DB_USER=${DB_USER}/g
find ${ROOT_DIR}/docker.env -type f -name "*" | xargs sed -i'' s/DB_PASSWORD=/DB_PASSWORD=${DB_PASSWORD}/g
find ${ROOT_DIR}/docker.env -type f -name "*" | xargs sed -i'' s/DB_NAME=/DB_NAME=${DB_NAME}/g

echo preprocess docker compose files
cp -f ${ROOT_DIR}/ci/docker-compose.yml.template ${ROOT_DIR}/docker-compose.yml
echo ${ROOT_DIR}/docker-compose.yml
find ${ROOT_DIR}/docker-compose.yml -type f -name "*" | xargs sed -i'' s/__WEB_PORT__/${WEB_PORT}/g

echo preprocess docker file
cp -f ${ROOT_DIR}/ci/Dockerfile.template ${ROOT_DIR}/Dockerfile

# Backend config
echo preprocess config.env
cp -f ${BACKEND_DIR}/config.env.template ${BACKEND_DIR}/config.env
# App
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/APP_NAME=/APP_NAME=${APP_NAME}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/SECRET_KEY=/SECRET_KEY=${SECRET_KEY}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DEBUG=/DEBUG=${DEBUG}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s%OIDC_RSA_PRIVATE_KEY_FILE=%OIDC_RSA_PRIVATE_KEY_FILE=${OIDC_RSA_PRIVATE_KEY_FILE}%g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s%JWT_ISSUER=%JWT_ISSUER=${JWT_ISSUER}%g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/LOCAL_BUILD=/LOCAL_BUILD=${LOCAL_BUILD}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s%DEFAULT_HOST=%DEFAULT_HOST=${DEFAULT_HOST}%g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s%BUSINESS_HOST=%BUSINESS_HOST=${BUSINESS_HOST}%g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/BUSINESS_FRONTEND_DEV_MODE=/BUSINESS_FRONTEND_DEV_MODE=${BUSINESS_FRONTEND_DEV_MODE}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s%DOCS_HOST=%DOCS_HOST=${DOCS_HOST}%g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DOCS_FRONTEND_DEV_MODE=/DOCS_FRONTEND_DEV_MODE=${DOCS_FRONTEND_DEV_MODE}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/CORS_ALLOW_ALL_ORIGINS=/CORS_ALLOW_ALL_ORIGINS=${CORS_ALLOW_ALL_ORIGINS}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s%CORS_ALLOWED_ORIGINS=%CORS_ALLOWED_ORIGINS=${CORS_ALLOWED_ORIGINS}%g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DJANGO_ALLOWED_HOSTS=/DJANGO_ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/USE_X_FORWARDED_HOST=/USE_X_FORWARDED_HOST=${USE_X_FORWARDED_HOST}/g
# Database
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DB_HOST=/DB_HOST=${DB_HOST}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DB_PORT=/DB_PORT=${DB_PORT}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DB_USER=/DB_USER=${DB_USER}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DB_PASSWORD=/DB_PASSWORD=${DB_PASSWORD}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DB_NAME=/DB_NAME=${DB_NAME}/g
# OpenSearch
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s%OPEN_SEARCH_HOST=%OPEN_SEARCH_HOST=${OPEN_SEARCH_HOST}%g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/OPEN_SEARCH_SECURE_SCHEME=/OPEN_SEARCH_SECURE_SCHEME=${OPEN_SEARCH_SECURE_SCHEME}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s%OPEN_SEARCH_SECURE_HOST=%OPEN_SEARCH_SECURE_HOST=${OPEN_SEARCH_SECURE_HOST}%g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/OPEN_SEARCH_SECURE_PORT=/OPEN_SEARCH_SECURE_PORT=${OPEN_SEARCH_SECURE_PORT}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/OPEN_SEARCH_USER=/OPEN_SEARCH_USER=${OPEN_SEARCH_USER}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/OPEN_SEARCH_PASSWORD=/OPEN_SEARCH_PASSWORD=${OPEN_SEARCH_PASSWORD}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/OPEN_SEARCH_TIMEOUT=/OPEN_SEARCH_TIMEOUT=${OPEN_SEARCH_TIMEOUT}/g
# Rasa
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s%RASA_ENDPOINT=%RASA_ENDPOINT=${DB_HOST}%g
# Default accounts
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/BUSINESS_CLIENT_ID=/BUSINESS_CLIENT_ID=${BUSINESS_CLIENT_ID}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/BUSINESS_CLIENT_SECRET=/BUSINESS_CLIENT_SECRET=${BUSINESS_CLIENT_SECRET}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/ECOMMERCE_CLIENT_ID=/ECOMMERCE_CLIENT_ID=${ECOMMERCE_CLIENT_ID}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/ECOMMERCE_CLIENT_SECRET=/ECOMMERCE_CLIENT_SECRET=${ECOMMERCE_CLIENT_SECRET}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/SUPER_ADMIN_EMAIL=/SUPER_ADMIN_EMAIL=${SUPER_ADMIN_EMAIL}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/SUPER_ADMIN_PASSWORD=/SUPER_ADMIN_PASSWORD=${SUPER_ADMIN_PASSWORD}/g
# Email
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/EMAIL_HOST=/EMAIL_HOST=${EMAIL_HOST}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/EMAIL_PORT=/EMAIL_PORT=${EMAIL_PORT}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/EMAIL_HOST_USER=\'\'/EMAIL_HOST_USER=\'${EMAIL_HOST_USER}\'/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/EMAIL_HOST_PASSWORD=\'\'/EMAIL_HOST_PASSWORD=\'${EMAIL_HOST_PASSWORD}\'/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s%BLOCKED_EMAIL_DOMAINS=%BLOCKED_EMAIL_DOMAINS=${BLOCKED_EMAIL_DOMAINS}%g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DEFAULT_FROM_EMAIL=/DEFAULT_FROM_EMAIL=${DEFAULT_FROM_EMAIL}/g
# API documents
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/ALLOWED_SWAGGER=/ALLOWED_SWAGGER=${ALLOWED_SWAGGER}/g
# Storage
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/FILE_UPLOAD_MAX_MEMORY_SIZE=/FILE_UPLOAD_MAX_MEMORY_SIZE=${FILE_UPLOAD_MAX_MEMORY_SIZE}/g
# AWS
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/AWS_ACCESS_KEY_ID=/AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/AWS_SECRET_ACCESS_KEY=/AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/STORE_USER_FILES_ON_S3=/STORE_USER_FILES_ON_S3=${STORE_USER_FILES_ON_S3}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/AWS_STORAGE_BUCKET_NAME=/AWS_STORAGE_BUCKET_NAME=${AWS_STORAGE_BUCKET_NAME}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/AWS_S3_REGION_NAME=/AWS_S3_REGION_NAME=${AWS_S3_REGION_NAME}/g
#SMS
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/TWILIO_ACCOUNT_SID=/TWILIO_ACCOUNT_SID=${TWILIO_ACCOUNT_SID}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/TWILIO_AUTH_TOKEN=/TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/TWILIO_CALLER_ID=/TWILIO_CALLER_ID=${TWILIO_CALLER_ID}/g
find ${BACKEND_DIR}/config.env -type f -name "*" | xargs sed -i'' s/OTP_TOTP_SYNC=/OTP_TOTP_SYNC=${OTP_TOTP_SYNC}/g

# Create file private KEY
cd $BACKEND_DIR
file="${BACKEND_DIR}/${OIDC_RSA_PRIVATE_KEY_FILE}"
echo $file
if [ -f "$file" ]
then
	echo "File ${file}.key is already exists"
else
	openssl genrsa -out "${file}" 4096
	chmod 777 "${file}"
fi

echo "Done."
