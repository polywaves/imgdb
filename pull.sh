#!/bin/bash

git stash
git pull
# docker -f docker-compose.prod.yml compose down
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml logs -f api