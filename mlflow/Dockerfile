FROM python:3.9-slim

RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install mlflow boto3 psycopg2-binary