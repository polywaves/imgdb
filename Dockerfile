FROM python:3.10-slim

RUN apt-get update
RUN apt-get install -y curl

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

COPY . .

COPY download_model.py .
RUN chmod +x download_model.py && ./download_model.py

CMD uvicorn main:app --port 8081 --host=0.0.0.0 --use-colors