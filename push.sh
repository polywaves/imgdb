#!/bin/bash

docker build -t polywaves/api .
docker push polywaves/api

docker build -t polywaves/i2v ./i2v
docker push polywaves/i2v

git add .
git commit -m update
git push