# syntax=docker/dockerfile:1

FROM python:3.9-alpine3.16

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --update --no-cache curl gcc musl-dev

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml README.md ./
COPY happy happy/

RUN poetry install

ENTRYPOINT ["poetry", "run", "uvicorn", "happy.main:app"]
