# syntax=docker/dockerfile:1

FROM python:3.9-alpine3.16

ENV TZ=Europe/Paris
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --update --no-cache curl gcc musl-dev ca-certificates \
    && update-ca-certificates

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml README.md ./
COPY happy happy/

RUN poetry install

ENTRYPOINT ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "80", "happy.main:app"]
