# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.9-slim-buster
LABEL maintainer "Ivan Skvortsov <iaskvortsov@edu.hse.ru>"

WORKDIR /app
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install "poetry" && poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /app/
COPY . ./

RUN poetry install

#CMD [ "pwd" ]
CMD [ "poetry", "run" , "python3", "__init__.py" ]

# WORKDIR /ml_models
# WORKDIR /executions