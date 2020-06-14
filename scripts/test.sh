#!/usr/bin/env bash
set -e

poetry run pytest --cov=fastapi_code_generator --cov-report term-missing tests