#!/usr/bin/env bash
set -e

cp README.md docs/index.md
pytest --collect-cli-docs -p no:xdist -q
python scripts/build_cli_docs.py
mkdocs build --verbose --clean --strict
