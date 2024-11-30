#!/bin/bash
echo “Starting server...”
cd /home/ec2-user/projects/secret-friend
/usr/local/bin/docker-compose -f docker-compose.yml up -d --build