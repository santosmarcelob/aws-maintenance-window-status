#!/bin/bash
sudo yum update -y
sudo yum install -y python3
sudo yum install -y python3-pip
sudo pip3 install flask
sudo mkdir -p /home/ec2-user/myapp/templates/
sudo mkdir -p /home/ec2-user/myapp/static/styles/
sudo chown ec2-user:ec2-user /home/ec2-user/myapp/
sudo chown ec2-user:ec2-user /home/ec2-user/myapp/templates/
sudo chown ec2-user:ec2-user /home/ec2-user/myapp/static/
sudo chown ec2-user:ec2-user /home/ec2-user/myapp/static/styles/
sudo mv /tmp/app.py /home/ec2-user/myapp
sudo mv /tmp/index.html /home/ec2-user/myapp/templates
sudo mv /tmp/style.css /home/ec2-user/myapp/static/styles
sudo mv /tmp/scripts.js /home/ec2-user/myapp/static