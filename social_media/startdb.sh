#!/bin/bash

brew services stop postgresql@15
# Start the project in detached mode
docker-compose up -d
