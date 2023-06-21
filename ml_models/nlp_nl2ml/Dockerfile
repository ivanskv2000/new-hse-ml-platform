# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.8.0-slim
LABEL maintainer "Ivan Skvortsov <iaskvortsov@edu.hse.ru>"

WORKDIR /model

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install "poetry" && poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /model/
COPY . ./

RUN poetry install

CMD [ "poetry", "run" , "python3", "nlp_nl2ml_api.py"]