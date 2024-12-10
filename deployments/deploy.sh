#!/bin/bash

# Setup the env variables
set -a
source ~/mess_manager/env/.env
set +a

# Stop and remove existing container
docker stop mess_app_server || true
docker rm mess_app_server || true

# Delete existing image
docker rmi adityaupadhye/mess-manager-server:latest || true

echo "Docker cleanup done. Pulling new image from Docker Hub..."

# Pull the latest image from Docker Hub
docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"
docker pull adityaupadhye/mess-manager-server:latest

# Run the new container
docker run -d \
 -p 8080:8080 \
 --name mess_app_server \
 --restart unless-stopped \
 --env-file ~/mess_manager/env/.env \
 -v ~/mess_manager/env/.env:/app/.env \
 adityaupadhye/mess-manager-server:latest

echo "Docker container 'mess_app_server' up and running..."

# Setup Django crontabs
docker exec mess_app_server sh -c "python3 manage.py crontab add &"
