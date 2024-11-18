FROM python:3.11-slim

RUN apt-get update
RUN apt-get install -y curl

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD uvicorn main:app --port 8080 --host=0.0.0.0 --use-colors --reload