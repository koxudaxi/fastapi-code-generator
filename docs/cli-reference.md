# CLI Reference

This page is generated from the current `fastapi-codegen --help` output.
Run `tox run -e cli-docs` after changing CLI options.

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
  --reuse-model                   Reuse identical generated models as the same
                                  type.
  --enable-faux-immutability      Generate frozen Pydantic models so instances
                                  are hashable when their fields are hashable.
  --install-completion            Install completion for the current shell.
  --show-completion               Show completion for the current shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

## Tested CLI Scenarios

### --help

Show the CLI help message.

`fastapi-codegen --help`

### --version

Show the installed fastapi-codegen version.

`fastapi-codegen --version`

### --output

Directory where the generated FastAPI application is written.

`fastapi-codegen --input openapi/default_template/simple.yaml --output app`

Input schema: `openapi/default_template/simple.yaml`

Related options: `--input`

### --input

Generate a FastAPI application from an OpenAPI input file.

`fastapi-codegen --input openapi/default_template/simple.yaml --output app`

Input schema: `openapi/default_template/simple.yaml`

Related options: `--output`

### --template-dir

Render generated files with a custom template directory.

`fastapi-codegen --input openapi/custom_template_security/custom_security.yaml --output app --template-dir custom_template/security`

Input schema: `openapi/custom_template_security/custom_security.yaml`

### --include-request-argument

Auto-inject a FastAPI Request argument in generated operation signatures when not present.

`fastapi-codegen --input openapi/default_template/simple.yaml --output app --include-request-argument`

Input schema: `openapi/default_template/simple.yaml`

### --encoding

Read the input schema using an explicit text encoding.

`fastapi-codegen --input openapi/default_template/simple.yaml --output app --encoding utf-16`

Input schema: `openapi/default_template/simple.yaml`

### --disable-timestamp

Omit the generated timestamp header from output files.

`fastapi-codegen --input openapi/disable_timestamp/simple.yaml --output app --disable-timestamp`

Input schema: `openapi/disable_timestamp/simple.yaml`

### --strict-nullable

Respect explicit OpenAPI nullable flags when generating models.

`fastapi-codegen --input openapi/default_template/nullable_test.yaml --output app --strict-nullable`

Input schema: `openapi/default_template/nullable_test.yaml`

### --generate-routers

Generate modular router files from tagged OpenAPI operations.

`fastapi-codegen --input openapi/using_routers/using_routers_example.yaml --output app --template-dir modular_template --generate-routers`

Input schema: `openapi/using_routers/using_routers_example.yaml`

### --specify-tags

Generate or regenerate only the routers matching a comma-separated tag list.

`fastapi-codegen --input openapi/using_routers/using_routers_example.yaml --output app --template-dir modular_template --generate-routers --specify-tags Wild Boars, Fat Cats`

Input schema: `openapi/using_routers/using_routers_example.yaml`

### --enum-field-as-literal

Render enum fields as Literal annotations.

`fastapi-codegen --input openapi/default_template/duplicate_anonymus_parameter.yaml --output app --enum-field-as-literal all`

Input schema: `openapi/default_template/duplicate_anonymus_parameter.yaml`

### --use-annotated

Render model field constraints with typing.Annotated.

`fastapi-codegen --input openapi/default_template/recursion.yaml --output app --use-annotated`

Input schema: `openapi/default_template/recursion.yaml`

### --enable-faux-immutability

Generate frozen Pydantic models so instances are hashable when their fields are hashable.

`fastapi-codegen --input openapi/coverage/faux_immutability.yaml --output app --enable-faux-immutability`

Input schema: `openapi/coverage/faux_immutability.yaml`

### --model-file

Write generated models to a custom module path.

`fastapi-codegen --input openapi/default_template/body_and_parameters.yaml --output app --model-file custom_models.py --model-template-dir model_templates --output-model-type pydantic_v2.BaseModel --python-version 3.13`

Input schema: `openapi/default_template/body_and_parameters.yaml`

Related options: `--model-template-dir`, `--output-model-type`, `--python-version`

### --model-template-dir

Use a custom datamodel-code-generator template directory.

`fastapi-codegen --input openapi/default_template/body_and_parameters.yaml --output app --model-file custom_models.py --model-template-dir model_templates --output-model-type pydantic_v2.BaseModel --python-version 3.13`

Input schema: `openapi/default_template/body_and_parameters.yaml`

Related options: `--model-file`, `--output-model-type`, `--python-version`

### --output-model-type

Choose the datamodel-code-generator output backend.

`fastapi-codegen --input openapi/default_template/body_and_parameters.yaml --output app --model-file custom_models.py --model-template-dir model_templates --output-model-type pydantic_v2.BaseModel --python-version 3.13`

Input schema: `openapi/default_template/body_and_parameters.yaml`

Related options: `--model-file`, `--model-template-dir`, `--python-version`

### --python-version

Target a specific Python version when formatting generated code.

`fastapi-codegen --input openapi/default_template/body_and_parameters.yaml --output app --model-file custom_models.py --model-template-dir model_templates --output-model-type pydantic_v2.BaseModel --python-version 3.13`

Input schema: `openapi/default_template/body_and_parameters.yaml`

Related options: `--model-file`, `--model-template-dir`, `--output-model-type`

### --reuse-model

Reuse generated model classes when another model has the same content.

`fastapi-codegen --input openapi/default_template/reuse_model.yaml --output app --reuse-model`

Input schema: `openapi/default_template/reuse_model.yaml`

Related options: `--model-file`, `--output-model-type`

### --custom-visitor

Load a custom visitor module and expose additional template variables.

`fastapi-codegen --input openapi/default_template/simple.yaml --output app --template-dir template --generate-routers --custom-visitor visitor.py`

Input schema: `openapi/default_template/simple.yaml`
