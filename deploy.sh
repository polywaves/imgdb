#!/bin/bash

docker build -t polywaves/api .
docker push polywaves/api

docker build -t polywaves/nginx ./nginx
docker push polywaves/nginx

git add .
git commit -m update
git push