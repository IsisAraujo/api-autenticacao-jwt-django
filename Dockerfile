FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip install -U pip setuptools poetry
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /code/
RUN poetry install --no-root

COPY . /code/
