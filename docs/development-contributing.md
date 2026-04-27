# Development and Contributing

The `docs/` directory is the source of truth for user-facing documentation. Keep `README.md`, the docs overview, the generated CLI reference, and the `llms.txt` files in sync when you touch the CLI or docs structure.

## Local Setup

```bash
# 1. Clone your fork
git clone git@github.com:<your-username>/fastapi-code-generator.git
cd fastapi-code-generator

# 2. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install tox with uv
uv tool install --python-preference only-managed --python 3.14 tox --with tox-uv

# 4. Create a development environment
tox run -e dev

# 5. Install pre-commit hooks
pre-commit install
```

## Day-to-Day Workflow

```bash
# 1. Create a branch
git checkout -b my-change

# 2. Run the CLI and code generation tests
tox run -e py314-parallel

# 3. Format the code base
tox run -e fix

# 4. Run type checks
tox run -e type

# 5. Refresh the README and docs overview CLI help snapshots
python scripts/update_command_help_on_markdown.py

# 6. Rebuild the generated CLI reference
tox run -e cli-docs

# 7. Refresh generated docs artifacts
tox run -e readme
tox run -e llms-txt
tox run -e schema-docs
tox run -e config-types

# 8. Build the documentation site
tox run -e docs

# 9. Build package metadata
tox run -e pkg_meta
```

## Validation Checklist

Run the check variants before opening a pull request when your change touches CLI help, docs content, or docs navigation:

```bash
tox run -e py314-parallel
tox run -e fix
tox run -e type
tox run -e readme -- --check
tox run -e cli-docs -- --check
tox run -e llms-txt -- --check
tox run -e schema-docs -- --check
tox run -e config-types -- --check
tox run -e docs
tox run -e pkg_meta
```

If you need combined local coverage, run:

```bash
tox run -e coverage
```

## Docs Maintenance Notes

- Update `zensical.toml` whenever the docs nav changes
- Keep `docs/index.md` as the canonical long-form overview instead of copying `README.md` into docs
- Regenerate `docs/cli-reference.md` after CLI option changes
- Regenerate `docs/llms.txt` and `docs/llms-full.txt` after docs page or nav changes
