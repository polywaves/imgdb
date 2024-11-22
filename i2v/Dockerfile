FROM python:3.11-slim

RUN apt-get update
RUN apt-get install -y curl

WORKDIR /app

RUN pip install --upgrade pip setuptools
COPY requirements.txt .
RUN pip install -r requirements.txt

ARG MODEL_NAME
COPY download_model.py .
RUN ./download_model.py

COPY . .

ENTRYPOINT /bin/sh -c
CMD uvicorn app:app --port 8080 --host=0.0.0.0 --use-colors