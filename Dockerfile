FROM python:latest

WORKDIR /usr/src/drand

COPY . .

RUN pip install --editable .[dev]
