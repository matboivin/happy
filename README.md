# Happy ᕕ( ՞ ᗜ ՞ )ᕗ

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) [![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

A basic `FastAPI` application using ElasticSearch.

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Environment variables](#environment-variables)
4. [Usage](#usage)
5. [Development](#development)

## Prerequisites

- GNU make
- Docker and Docker compose

## Installation

Clone the repository and change it to your working directory.

Set the environment variables in a `.env` file. An example file is located at the root of the repository.

```bash
# .env or .dev.env
ENV=

STACK_VERSION=

ELASTICSEARCH_HOST=
ELASTICSEARCH_PORT=
ELASTICSEARCH_USERNAME=
ELASTICSEARCH_PASSWORD=
KIBANA_PASSWORD=
```

## Usage

```console
$ make ENV=production up-build
```

## Development

### Prerequisites

- [poetry](https://python-poetry.org)

## Usage

```console
# Development is the default environment
$ make up-build
```

In development, the source files are passed to the `Happy` container as volumes. The server will restart every time a file is edited.
