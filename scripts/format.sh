#!/usr/bin/env bash
set -e

uv run --group lint black fastapi_code_generator tests
uv run --group lint isort --recursive fastapi_code_generator tests
