#!/bin/sh

# This script performs all the actions to start the docker instances 
# and other actions that are required for starting up the project

# Delete old migrations
rm -rf ./backend/migrations

# Start the docker instances
docker-compose up