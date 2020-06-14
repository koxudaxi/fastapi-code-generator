#!/usr/bin/env bash
set -e

cp README.md docs/index.md && mkdocs build --verbose --clean --strict