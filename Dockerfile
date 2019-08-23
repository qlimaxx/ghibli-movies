FROM python:3.7-alpine

WORKDIR /code

COPY requirements.txt ./
COPY requirements-dev.txt ./

RUN pip3 install --upgrade pip && pip3 install -r requirements-dev.txt
