#!/bin/bash

# This is a script to setup and deploy a Discord Bot server
sudo apt update
sudo apt upgrade
sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3 python3-dev python3-venv python3-pip -y

# Directory making for Bot
sudo mkdir DiscordBot
cd DiscordBot
sudo python3 -m venv ./venv
source ./venv/bin/activate

# This is after you uploaded and transferred the files via FTP
# sudo pip install discord.py python-dotenv
# also need to install NPM at this time manual install while script is being written