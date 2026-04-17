# CLI Reference

This page is generated from the current `fastapi-codegen --help` output.
Run `tox run -e cli-docs` after changing CLI options.

```text
Usage: fastapi-codegen [OPTIONS]                                                             
                                                                                              
╭─ Options ──────────────────────────────────────────────────────────────────────────────────╮
│    --encoding               -e      TEXT                        [default: utf-8]           │
│ *  --input                  -i      TEXT                        [required]                 │
│ *  --output                 -o      PATH                        [required]                 │
│    --model-file             -m      TEXT                                                   │
│    --template-dir           -t      PATH                                                   │
│    --model-template-dir             PATH                                                   │
│    --enum-field-as-literal          [all|one]                                              │
│    --generate-routers       -r                                                             │
│    --specify-tags                   TEXT                                                   │
│    --custom-visitor         -c      PATH                                                   │
│    --disable-timestamp                                                                     │
│    --output-model-type      -d      [pydantic.BaseModel|pydant  [default:                  │
│                                     ic_v2.BaseModel|dataclasse  pydantic.BaseModel]        │
│                                     s.dataclass|typing.TypedDi                             │
│                                     ct|msgspec.Struct]                                     │
│    --python-version         -p      [3.9|3.10|3.11|3.12|3.13|3  [default: 3.10]            │
│                                     .14]                                                   │
│    --install-completion                                         Install completion for the │
│                                                                 current shell.             │
│    --show-completion                                            Show completion for the    │
│                                                                 current shell, to copy it  │
│                                                                 or customize the           │
│                                                                 installation.              │
│    --help                                                       Show this message and      │
│                                                                 exit.                      │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Tested CLI Scenarios

### --help

Show the CLI help message.

`fastapi-codegen --help`

### --version

Show the installed fastapi-codegen version.

`fastapi-codegen --version`

### --input, --output

Generate a FastAPI application from an OpenAPI input file.

`fastapi-codegen --input openapi/default_template/simple.yaml --output app`

Input schema: `openapi/default_template/simple.yaml`

### --template-dir

Render generated files with a custom template directory.

`fastapi-codegen --input openapi/custom_template_security/custom_security.yaml --output app --template-dir custom_template/security`

Input schema: `openapi/custom_template_security/custom_security.yaml`

### --encoding

Read the input schema using an explicit text encoding.

`fastapi-codegen --input openapi/default_template/simple.yaml --output app --encoding utf-16`

Input schema: `openapi/default_template/simple.yaml`

### --disable-timestamp

Omit the generated timestamp header from output files.

`fastapi-codegen --input openapi/disable_timestamp/simple.yaml --output app --disable-timestamp`

Input schema: `openapi/disable_timestamp/simple.yaml`

### --generate-routers

Generate modular router files from tagged OpenAPI operations.

`fastapi-codegen --input openapi/using_routers/using_routers_example.yaml --output app --template-dir modular_template --generate-routers`

Input schema: `openapi/using_routers/using_routers_example.yaml`

### --specify-tags

Regenerate only the routers matching a comma-separated tag list.

`fastapi-codegen --input openapi/using_routers/using_routers_example.yaml --output app --template-dir modular_template --generate-routers --specify-tags Wild Boars, Fat Cats`

Input schema: `openapi/using_routers/using_routers_example.yaml`

### --enum-field-as-literal

Render enum fields as Literal annotations.

`fastapi-codegen --input openapi/default_template/duplicate_anonymus_parameter.yaml --output app --enum-field-as-literal all`

Input schema: `openapi/default_template/duplicate_anonymus_parameter.yaml`

### --model-file, --model-template-dir, --output-model-type, --python-version

Customize generated model paths and datamodel-code-generator output settings.

`fastapi-codegen --input openapi/default_template/body_and_parameters.yaml --output app --model-file custom_models.py --model-template-dir model_templates --output-model-type pydantic_v2.BaseModel --python-version 3.13`

Input schema: `openapi/default_template/body_and_parameters.yaml`

### --custom-visitor

Load a custom visitor module and expose additional template variables.

`fastapi-codegen --input openapi/default_template/simple.yaml --output app --template-dir template --generate-routers --custom-visitor visitor.py`

Input schema: `openapi/default_template/simple.yaml`
