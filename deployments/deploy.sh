#!/bin/bash

# stop and remove existing container
docker stop mess_app_server || true
docker rm mess_app_server || true

# delete existing image
docker rmi mess_app || true

echo "docker cleanup done. Building new image"

# create new image
docker build -t mess_app .

echo "New docker image ready"

# run new container
docker run -d \
 -p 8080:8080 \
 --name mess_app_server \
 --restart unless-stopped \
 mess_app

echo "Docker container `mess_app_server` up and running..."

# setup django crontabs
docker exec mess_app_server sh -c "python3 manage.py crontab add &"