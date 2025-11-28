FROM jupyter/base-notebook:python-3.9

USER root
RUN apt-get update && apt-get install -y libpq-dev gcc

USER jovyan
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt