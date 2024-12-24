FROM python:3.11-slim

RUN apt-get update
RUN apt-get install -y curl

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN curl -fsSL https://get.docker.com | sh

COPY . .

CMD uvicorn main:app --port 8081 --host=0.0.0.0 --use-colors