#!/bin/sh
#
# Docker entrypoint

set -e

poetry install
poetry run uvicorn --host "0.0.0.0" --port 80 --reload happy.main:app
