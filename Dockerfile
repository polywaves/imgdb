FROM python:3.10-buster

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT uvicorn main:app --port 80 --host=0.0.0.0 --use-colors --reload