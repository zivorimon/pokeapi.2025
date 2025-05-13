#!/bin/bash
# Update system
sudo apt update -y
sudo apt install -y python3 python3-pip git

# clone git ripo

git clone https://github.com/zivorimon/pokeapi.2025/tree/master

# run the game automatic
echo "cd ~/pokemon-game && python3 user_controller.py"