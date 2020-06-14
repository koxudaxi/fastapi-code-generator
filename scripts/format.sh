#!/usr/bin/env bash
set -e

poetry run black fastapi_code_generator tests
poetry run isort --recursive fastapi_code_generator tests
