#!/bin/bash

docker compose up -d --build
docker compose logs -f