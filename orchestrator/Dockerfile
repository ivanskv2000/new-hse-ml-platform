# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster
LABEL maintainer "Ivan Skvortsov <iaskvortsov@edu.hse.ru>"

WORKDIR /app
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install "poetry==1.2.2" && poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /app/
COPY . ./

RUN poetry install

CMD [ "poetry", "run" , "python3", "__init__.py"]

WORKDIR /ml_models
WORKDIR /executions