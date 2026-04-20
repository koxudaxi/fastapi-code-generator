{
  "project": "fastapi-code-generator",
  "entrypoint": "fastapi-codegen",
  "config_options": [
    {
      "name": "encoding",
      "cli_flags": [
        "--encoding",
        "-e"
      ],
      "description": "Text encoding used to read the input OpenAPI document.",
      "required": false,
      "default": "utf-8",
      "multiple": false,
      "type": "string",
      "choices": []
    },
    {
      "name": "input_file",
      "cli_flags": [
        "--input",
        "-i"
      ],
      "description": "Path to the OpenAPI input document.",
      "required": true,
      "default": null,
      "multiple": false,
      "type": "string",
      "choices": []
    },
    {
      "name": "output_dir",
      "cli_flags": [
        "--output",
        "-o"
      ],
      "description": "Directory where the generated FastAPI application is written.",
      "required": true,
      "default": null,
      "multiple": false,
      "type": "string",
      "choices": []
    },
    {
      "name": "model_file",
      "cli_flags": [
        "--model-file",
        "-m"
      ],
      "description": "Optional output path for the generated model module.",
      "required": false,
      "default": null,
      "multiple": false,
      "type": "string | null",
      "choices": []
    },
    {
      "name": "template_dir",
      "cli_flags": [
        "--template-dir",
        "-t"
      ],
      "description": "Optional custom template directory for application files.",
      "required": false,
      "default": null,
      "multiple": false,
      "type": "string | null",
      "choices": []
    },
    {
      "name": "model_template_dir",
      "cli_flags": [
        "--model-template-dir"
      ],
      "description": "Optional custom datamodel-code-generator template directory.",
      "required": false,
      "default": null,
      "multiple": false,
      "type": "string | null",
      "choices": []
    },
    {
      "name": "enum_field_as_literal",
      "cli_flags": [
        "--enum-field-as-literal"
      ],
      "description": "Render enum-like values as Literal annotations.",
      "required": false,
      "default": null,
      "multiple": false,
      "type": "literal | null",
      "choices": [
        "all",
        "one"
      ]
    },
    {
      "name": "generate_routers",
      "cli_flags": [
        "--generate-routers",
        "-r"
      ],
      "description": "Generate router modules with the modular template.",
      "required": false,
      "default": false,
      "multiple": false,
      "type": "boolean",
      "choices": []
    },
    {
      "name": "specify_tags",
      "cli_flags": [
        "--specify-tags"
      ],
      "description": "Comma-separated router tags to regenerate with modular output.",
      "required": false,
      "default": null,
      "multiple": false,
      "type": "string | null",
      "choices": []
    },
    {
      "name": "custom_visitors",
      "cli_flags": [
        "--custom-visitor",
        "-c"
      ],
      "description": "Additional visitor module paths that inject template variables.",
      "required": false,
      "default": null,
      "multiple": true,
      "type": "list[string] | null",
      "choices": []
    },
    {
      "name": "disable_timestamp",
      "cli_flags": [
        "--disable-timestamp"
      ],
      "description": "Omit timestamp headers from generated files.",
      "required": false,
      "default": false,
      "multiple": false,
      "type": "boolean",
      "choices": []
    },
    {
      "name": "output_model_type",
      "cli_flags": [
        "--output-model-type",
        "-d"
      ],
      "description": "Model backend passed through to datamodel-code-generator.",
      "required": false,
      "default": "pydantic.BaseModel",
      "multiple": false,
      "type": "literal",
      "choices": [
        "pydantic.BaseModel",
        "pydantic_v2.BaseModel",
        "dataclasses.dataclass",
        "typing.TypedDict",
        "msgspec.Struct"
      ]
    },
    {
      "name": "python_version",
      "cli_flags": [
        "--python-version",
        "-p"
      ],
      "description": "Target Python version used when formatting generated code.",
      "required": false,
      "default": "3.10",
      "multiple": false,
      "type": "literal",
      "choices": [
        "3.9",
        "3.10",
        "3.11",
        "3.12",
        "3.13",
        "3.14"
      ]
    }
  ],
  "cli_examples": [
    {
      "options": [
        "--help"
      ],
      "description": "Show the CLI help message.",
      "cli_args": [
        "--help"
      ],
      "input_schema": null
    },
    {
      "options": [
        "--version"
      ],
      "description": "Show the installed fastapi-codegen version.",
      "cli_args": [
        "--version"
      ],
      "input_schema": null
    },
    {
      "options": [
        "--input",
        "--output"
      ],
      "description": "Generate a FastAPI application from an OpenAPI input file.",
      "cli_args": [
        "--input",
        "openapi/default_template/simple.yaml",
        "--output",
        "app"
      ],
      "input_schema": "openapi/default_template/simple.yaml"
    },
    {
      "options": [
        "--template-dir"
      ],
      "description": "Render generated files with a custom template directory.",
      "cli_args": [
        "--input",
        "openapi/custom_template_security/custom_security.yaml",
        "--output",
        "app",
        "--template-dir",
        "custom_template/security"
      ],
      "input_schema": "openapi/custom_template_security/custom_security.yaml"
    },
    {
      "options": [
        "--encoding"
      ],
      "description": "Read the input schema using an explicit text encoding.",
      "cli_args": [
        "--input",
        "openapi/default_template/simple.yaml",
        "--output",
        "app",
        "--encoding",
        "utf-16"
      ],
      "input_schema": "openapi/default_template/simple.yaml"
    },
    {
      "options": [
        "--disable-timestamp"
      ],
      "description": "Omit the generated timestamp header from output files.",
      "cli_args": [
        "--input",
        "openapi/disable_timestamp/simple.yaml",
        "--output",
        "app",
        "--disable-timestamp"
      ],
      "input_schema": "openapi/disable_timestamp/simple.yaml"
    },
    {
      "options": [
        "--generate-routers"
      ],
      "description": "Generate modular router files from tagged OpenAPI operations.",
      "cli_args": [
        "--input",
        "openapi/using_routers/using_routers_example.yaml",
        "--output",
        "app",
        "--template-dir",
        "modular_template",
        "--generate-routers"
      ],
      "input_schema": "openapi/using_routers/using_routers_example.yaml"
    },
    {
      "options": [
        "--specify-tags"
      ],
      "description": "Regenerate only the routers matching a comma-separated tag list.",
      "cli_args": [
        "--input",
        "openapi/using_routers/using_routers_example.yaml",
        "--output",
        "app",
        "--template-dir",
        "modular_template",
        "--generate-routers",
        "--specify-tags",
        "Wild Boars, Fat Cats"
      ],
      "input_schema": "openapi/using_routers/using_routers_example.yaml"
    },
    {
      "options": [
        "--enum-field-as-literal"
      ],
      "description": "Render enum fields as Literal annotations.",
      "cli_args": [
        "--input",
        "openapi/default_template/duplicate_anonymus_parameter.yaml",
        "--output",
        "app",
        "--enum-field-as-literal",
        "all"
      ],
      "input_schema": "openapi/default_template/duplicate_anonymus_parameter.yaml"
    },
    {
      "options": [
        "--model-file",
        "--model-template-dir",
        "--output-model-type",
        "--python-version"
      ],
      "description": "Customize generated model paths and datamodel-code-generator output settings.",
      "cli_args": [
        "--input",
        "openapi/default_template/body_and_parameters.yaml",
        "--output",
        "app",
        "--model-file",
        "custom_models.py",
        "--model-template-dir",
        "model_templates",
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--python-version",
        "3.13"
      ],
      "input_schema": "openapi/default_template/body_and_parameters.yaml"
    },
    {
      "options": [
        "--custom-visitor"
      ],
      "description": "Load a custom visitor module and expose additional template variables.",
      "cli_args": [
        "--input",
        "openapi/default_template/simple.yaml",
        "--output",
        "app",
        "--template-dir",
        "template",
        "--generate-routers",
        "--custom-visitor",
        "visitor.py"
      ],
      "input_schema": "openapi/default_template/simple.yaml"
    }
  ],
  "schema_fixture_suites": [
    {
      "directory": "default_template",
      "title": "Default template",
      "notes": "Core single-file generation scenarios exercised by the main CLI tests."
    },
    {
      "directory": "coverage",
      "title": "Coverage fixtures",
      "notes": "Focused fixtures for callbacks, non-200 responses, and other regression edges."
    },
    {
      "directory": "custom_template_security",
      "title": "Custom template overrides",
      "notes": "Template override coverage for `--template-dir`."
    },
    {
      "directory": "disable_timestamp",
      "title": "Timestamp suppression",
      "notes": "Fixtures that exercise `--disable-timestamp`."
    },
    {
      "directory": "remote_ref",
      "title": "Remote references",
      "notes": "Fixtures whose `$ref` targets are resolved over HTTP at test time."
    },
    {
      "directory": "using_routers",
      "title": "Router generation",
      "notes": "Fixtures that exercise modular output and router regeneration."
    }
  ],
  "schema_docs_preview": "# Supported Formats\n\nThis page is generated from repository fixture inventory and config metadata.\nRun `tox run -e schema-docs` after changing supported inputs or model backends.\n\n## Input Formats\n\n| Format | Status | Evidence | Notes |\n|--------|--------|----------|-------|\n| OpenAPI YAML | tested | `tests/data/openapi/**/*.yaml` (23 fixtures) | Primary fixture format exercised under `tests/data/openapi/**/*.yaml`. |\n| OpenAPI JSON | tested | `tests/main/test_main.py::test_generate_from_json_input` | Covered by the JSON conversion CLI test in `tests/main/test_main.py`. |\n| Remote HTTP `$ref` targets | tested | `tests/main/test_main.py::test_generate_remote_ref` | Covered by the remote `$ref` generation test against a live HTTP server. |\n\n## Fixture Suites\n\n| Suite | Fixtures | Example files | Notes |\n|-------|----------|---------------|-------|\n| Default template | 16 | `body_and_parameters.yaml`, `content_in_parameters.yaml`, `content_in_parameters_inline.yaml` | Core single-file generation scenarios exercised by the main CLI tests. |\n| Coverage fixtures | 3 | `callbacks.yaml`, `callbacks_with_operation_id.yaml`, `non_200_responses.yaml` | Focused fixtures for callbacks, non-200 responses, and other regression edges. |\n| Custom template overrides | 1 | `custom_security.yaml` | Template override coverage for `--template-dir`. |\n| Timestamp suppression | 1 | `simple.yaml` | Fixtures that exercise `--disable-timestamp`. |\n| Remote references | 1 | `body_and_parameters.yaml` | Fixtures whose `$ref` targets are resolved over HTTP at test time. |\n| Router generation | 1 | `using_routers_example.yaml` | Fixtures that exercise modular output and router regeneration. |\n\n## Output Model Types\n\n| Output model type | Status | Notes |\n|-------------------|--------|-------|\n| `pydantic.BaseModel` | supported | Classic Pydantic BaseModel output. |\n| `pydantic_v2.BaseModel` | supported | Pydantic v2 BaseModel output. |\n| `dataclasses.dataclass` | supported | Standard-library dataclass output. |\n| `typing.TypedDict` | supported | TypedDict-based model output. |\n| `msgspec.Struct` | supported | msgspec Struct output. |\n"
}
