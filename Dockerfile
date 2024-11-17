FROM python:3.11-slim

RUN apt-get update && apt-get install -y wget

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT uvicorn main:app --port 80 --host=0.0.0.0 --use-colors --reload