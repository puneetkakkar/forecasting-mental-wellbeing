#!/bin/sh

# Delete old migrations
rm -rf ./backend/migrations

# Start the docker instances
docker-compose up