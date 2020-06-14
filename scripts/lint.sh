#!/usr/bin/env bash

set -e

poetry run black --check fastapi_code_generator tests
poetry run isort --recursive --check-only fastapi_code_generator tests
poetry run mypy fastapi_code_generator
