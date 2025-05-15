#!/bin/bash
sudo yum update -y
sudo yum install -y git python3

# Clone your repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git /home/ec2-user/pokemon-game

# Optional: run something from the repo
cd /home/ec2-user/pokemon-game
python3 your_script.py
