#!/bin/bash

cd ~/Academics/cs699/mess-manager-server

# stop and remove existing container
docker stop mess_app_server || true
docker rm mess_app_server || true

# delete existing image
docker rmi mess_app || true

# create new image
docker build -t mess_app .

# run new container
docker run -d -p 8080:8080 --name mess_app_server mess_app
