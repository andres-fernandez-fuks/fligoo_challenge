#!/bin/bash

# Set environment variables
export DJANGO_PORT=8000
export POSTGRES_EXTERNAL_PORT=5433

# Display the values of the environment variables
echo "DJANGO_PORT set to: $DJANGO_PORT"
echo "POSTGRES_EXTERNAL_PORT set to: $POSTGRES_EXTERNAL_PORT"

# Run the Docker Compose command
docker compose -f local.yml run --rm --service-ports django.tic_tac_toe_api
