#!/bin/sh
#
# Docker entrypoint

set -e

poetry install
poetry run uvicorn --reload happy.main:app
