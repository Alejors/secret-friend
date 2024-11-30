#!/bin/bash
echo “Clear docker images...”
cd /home/ec2-user/projects/secret-friend
docker rmi --force $(docker images -f 'dangling=true' -q)