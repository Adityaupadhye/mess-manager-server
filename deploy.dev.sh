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

# run the mysql container if not running
mysql_container_name="mess_manager_mysql"

if docker ps --filter "name=$mysql_container_name" --filter "status=running" | grep -q "$mysql_container_name"; then
    echo "Container $mysql_container_name is running."
else
    echo "Container $mysql_container_name is not running."
    docker run -d \
    --name $mysql_container_name \
    -e MYSQL_ROOT_PASSWORD=manager \
    -v mess_manager_data:/var/lib/mysql \
    -p 3306:3306 \
    mysql:latest

fi

