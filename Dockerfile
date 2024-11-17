FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT uvicorn main:app --port 8080 --host=api --use-colors --reload