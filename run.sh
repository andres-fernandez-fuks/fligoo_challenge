#!/bin/bash

export DJANGO_PORT=8000
export POSTGRES_EXTERNAL_PORT=5433

if [[ "$*" == *"--build"* ]]; then
    docker compose -f ~/Documents/GitHub/fligoo_challenge/local.yml build
fi

gnome-terminal -- /bin/sh -c "cd ~/Documents/GitHub/fligoo_challenge/ && docker compose -f local.yml run --rm --service-ports django.tic_tac_toe_api"

sleep 2

container_name=$(docker ps --format "{{.Names}}" | grep "django.tic_tac_toe_api")

docker exec --user root -it $container_name bash
