#!/usr/bin/env bash
set -e

poetry run pytest --cov=fastapi_code_generator --cov-report=xml --cov-report term-missing tests