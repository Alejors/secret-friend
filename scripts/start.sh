#!/bin/bash
echo “Starting server...”
cd /home/ec2-user/projects/secret-friend
mkdir -p /logs

/usr/local/bin/docker-compose -f docker-compose.prod.yml build
/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
/usr/local/bin/docker-compose -f docker-compose.prod.yml exec api alembic upgrade head  > /logs/alembic_upgrade.log 2>&1
