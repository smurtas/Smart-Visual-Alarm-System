#!/bin/bash

sudo apt update
sudo apt install -y mosquitto mosquitto-clients python3-pip

sudo systemctl enable mosquitto
sudo systemctl start mosquitto

echo "Mosquitto MQTT broker installed and started."