#!/bin/bash

git pull
# docker -f docker-compose.prod.yml compose down
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml logs -f