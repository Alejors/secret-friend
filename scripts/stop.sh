#!/bin/bash
echo “Stoping server...”
cd /home/ec2-user/projects/secret-friend
/usr/local/bin/docker-compose -f docker-compose.yml stop