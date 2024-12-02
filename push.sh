#!/bin/bash

docker build -t polywaves/api .
docker push polywaves/api

git add .
git commit -m update
git push