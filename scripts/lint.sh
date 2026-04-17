#!/usr/bin/env bash

set -e

uv run --group lint black --check fastapi_code_generator tests
uv run --group lint isort --recursive --check-only fastapi_code_generator tests
uv run --group test --group type mypy fastapi_code_generator
