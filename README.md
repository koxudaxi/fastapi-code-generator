# fastapi-code-generator

Generate a FastAPI application from an OpenAPI document.

[![PyPI version](https://badge.fury.io/py/fastapi-code-generator.svg)](https://pypi.python.org/pypi/fastapi-code-generator)
[![Downloads](https://pepy.tech/badge/fastapi-code-generator/month)](https://pepy.tech/project/fastapi-code-generator)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-code-generator)](https://pypi.python.org/pypi/fastapi-code-generator)
[![codecov](https://codecov.io/gh/koxudaxi/fastapi-code-generator/branch/main/graph/badge.svg)](https://codecov.io/gh/koxudaxi/fastapi-code-generator)
![license](https://img.shields.io/github/license/koxudaxi/fastapi-code-generator.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> 📣 💼 Maintainer update: Open to opportunities. 🔗 [koxudaxi.dev](https://koxudaxi.dev/?utm_source=github_readme&utm_medium=top&utm_campaign=open_to_work)

## Documentation

The docs site is the source of truth for user-facing documentation:

- [Overview](https://fastapi-code-generator.koxudaxi.dev/)
- [CLI Reference](https://fastapi-code-generator.koxudaxi.dev/cli-reference/)
- [Supported Formats](https://fastapi-code-generator.koxudaxi.dev/supported_formats/)
- [Development & Contributing](https://fastapi-code-generator.koxudaxi.dev/development-contributing/)

Use this README as a quick start. The full examples, templating details, and development workflow live in `docs/`.

## Installation

```bash
uv tool install fastapi-code-generator
```

```bash
pip install fastapi-code-generator
```

## Quick Start

```bash
fastapi-codegen --input openapi.yaml --output app --output-model-type pydantic_v2.BaseModel
```

`fastapi-code-generator` uses [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator) to build the model layer. See the [overview guide](https://fastapi-code-generator.koxudaxi.dev/) for a complete end-to-end example, custom templates, custom visitors, and router generation.

## Command Help Snapshot

This block is generated from the current CLI so the README and docs overview stay aligned. For tested option scenarios and examples, use the [CLI reference page](https://fastapi-code-generator.koxudaxi.dev/cli-reference/).

<!-- start command help -->
```text
Usage: fastapi-codegen [OPTIONS]

Options:
  -e, --encoding TEXT             [default: utf-8]
  -i, --input TEXT                [required]
  -o, --output PATH               [required]
  -m, --model-file TEXT
  -t, --template-dir PATH
  --model-template-dir PATH
  --enum-field-as-literal [all|one|none]
  -r, --generate-routers
  --specify-tags TEXT
  -c, --custom-visitor PATH
  --disable-timestamp
  --strict-nullable               Respect explicit OpenAPI nullable flags when
                                  generating models.
  --include-request-argument      Auto-inject a FastAPI Request parameter into
                                  operations when not present.
  -d, --output-model-type [pydantic_v2.BaseModel|pydantic_v2.dataclass|dataclasses.dataclass|typing.TypedDict|msgspec.Struct]
                                  [default: pydantic_v2.BaseModel]
  -p, --python-version [3.10|3.11|3.12|3.13|3.14]
                                  [default: 3.10]
  -V, --version
  --use-annotated                 Use typing.Annotated for generated model
                                  field constraints.
  --enable-faux-immutability      Generate frozen Pydantic models so instances
                                  are hashable when their fields are hashable.
  --install-completion            Install completion for the current shell.
  --show-completion               Show completion for the current shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```
<!-- end command help -->

## Common Tasks

- Generate a single-file app from an OpenAPI spec: `fastapi-codegen --input openapi.yaml --output app`
- Generate router modules for larger applications: `fastapi-codegen --input openapi.yaml --output app --template-dir modular_template --generate-routers`
- Limit router regeneration to specific tags: `fastapi-codegen --input openapi.yaml --output app --template-dir modular_template --generate-routers --specify-tags "Wild Boars, Fat Cats"`
- Target Pydantic v2 output: `fastapi-codegen --input openapi.yaml --output app --output-model-type pydantic_v2.BaseModel`

## Further Reading

- [Overview](https://fastapi-code-generator.koxudaxi.dev/) for the full walkthrough and generated output example
- [CLI Reference](https://fastapi-code-generator.koxudaxi.dev/cli-reference/) for option-by-option behavior and tested scenarios
- [Supported Formats](https://fastapi-code-generator.koxudaxi.dev/supported_formats/) for the generated support matrix
- [Development & Contributing](https://fastapi-code-generator.koxudaxi.dev/development-contributing/) for the local workflow and docs maintenance steps
