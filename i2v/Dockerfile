FROM python:3.11-slim

RUN apt-get update

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

ARG MODEL_NAME
COPY download_model.py .
RUN chmod +x download_model.py
RUN ./download_model.py

COPY . .

CMD uvicorn app:app --port 8080 --host=0.0.0.0 --use-colors