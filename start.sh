#!/bin/sh
sleep 30
echo "Starting init script:"
date
sudo service mosquitto stop
cd /home/novellamaker/novellaDjango/
echo "Starting docker" "
sudo docker-compose up -d
