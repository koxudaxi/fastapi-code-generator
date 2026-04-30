from __future__ import annotations

from typing import Any

PROMPT_DATA: dict[str, Any] = {
    'project': 'fastapi-code-generator',
    'entrypoint': 'fastapi-codegen',
    'config_options': [
        {
            'name': 'encoding',
            'cli_flags': ['--encoding', '-e'],
            'description': 'Text encoding used to read the input OpenAPI ' 'document.',
            'required': False,
            'default': 'utf-8',
            'multiple': False,
            'type': 'string',
            'choices': [],
        },
        {
            'name': 'input_file',
            'cli_flags': ['--input', '-i'],
            'description': 'Path to the OpenAPI input document.',
            'required': True,
            'default': None,
            'multiple': False,
            'type': 'string',
            'choices': [],
        },
        {
            'name': 'output_dir',
            'cli_flags': ['--output', '-o'],
            'description': 'Directory where the generated FastAPI application '
            'is written.',
            'required': True,
            'default': None,
            'multiple': False,
            'type': 'string',
            'choices': [],
        },
        {
            'name': 'model_file',
            'cli_flags': ['--model-file', '-m'],
            'description': 'Optional output path for the generated model ' 'module.',
            'required': False,
            'default': None,
            'multiple': False,
            'type': 'string | null',
            'choices': [],
        },
        {
            'name': 'template_dir',
            'cli_flags': ['--template-dir', '-t'],
            'description': 'Optional custom template directory for '
            'application files.',
            'required': False,
            'default': None,
            'multiple': False,
            'type': 'string | null',
            'choices': [],
        },
        {
            'name': 'model_template_dir',
            'cli_flags': ['--model-template-dir'],
            'description': 'Optional custom datamodel-code-generator template '
            'directory.',
            'required': False,
            'default': None,
            'multiple': False,
            'type': 'string | null',
            'choices': [],
        },
        {
            'name': 'enum_field_as_literal',
            'cli_flags': ['--enum-field-as-literal'],
            'description': 'Render enum-like values as Literal annotations.',
            'required': False,
            'default': None,
            'multiple': False,
            'type': 'literal | null',
            'choices': ['all', 'one', 'none'],
        },
        {
            'name': 'generate_routers',
            'cli_flags': ['--generate-routers', '-r'],
            'description': 'Generate router modules with the modular ' 'template.',
            'required': False,
            'default': False,
            'multiple': False,
            'type': 'boolean',
            'choices': [],
        },
        {
            'name': 'specify_tags',
            'cli_flags': ['--specify-tags'],
            'description': 'Comma-separated router tags to regenerate with '
            'modular output.',
            'required': False,
            'default': None,
            'multiple': False,
            'type': 'string | null',
            'choices': [],
        },
        {
            'name': 'custom_visitors',
            'cli_flags': ['--custom-visitor', '-c'],
            'description': 'Additional visitor module paths that inject '
            'template variables.',
            'required': False,
            'default': None,
            'multiple': True,
            'type': 'list[string] | null',
            'choices': [],
        },
        {
            'name': 'disable_timestamp',
            'cli_flags': ['--disable-timestamp'],
            'description': 'Omit timestamp headers from generated files.',
            'required': False,
            'default': False,
            'multiple': False,
            'type': 'boolean',
            'choices': [],
        },
        {
            'name': 'strict_nullable',
            'cli_flags': ['--strict-nullable'],
            'description': 'Respect explicit OpenAPI nullable flags when '
            'generating models.',
            'required': False,
            'default': False,
            'multiple': False,
            'type': 'boolean',
            'choices': [],
        },
        {
            'name': 'include_request_argument',
            'cli_flags': ['--include-request-argument'],
            'description': 'Auto-inject a FastAPI Request argument in '
            'generated operation signatures when not present.',
            'required': False,
            'default': False,
            'multiple': False,
            'type': 'boolean',
            'choices': [],
        },
        {
            'name': 'output_model_type',
            'cli_flags': ['--output-model-type', '-d'],
            'description': 'Model backend passed through to '
            'datamodel-code-generator.',
            'required': False,
            'default': 'pydantic_v2.BaseModel',
            'multiple': False,
            'type': 'literal',
            'choices': [
                'pydantic_v2.BaseModel',
                'pydantic_v2.dataclass',
                'dataclasses.dataclass',
                'typing.TypedDict',
                'msgspec.Struct',
            ],
        },
        {
            'name': 'python_version',
            'cli_flags': ['--python-version', '-p'],
            'description': 'Target Python version used when formatting '
            'generated code.',
            'required': False,
            'default': '3.10',
            'multiple': False,
            'type': 'literal',
            'choices': ['3.10', '3.11', '3.12', '3.13', '3.14'],
        },
        {
            'name': 'use_annotated',
            'cli_flags': ['--use-annotated'],
            'description': 'Use `typing.Annotated` for generated model field '
            'constraints.',
            'required': False,
            'default': False,
            'multiple': False,
            'type': 'boolean',
            'choices': [],
        },
        {
            'name': 'reuse_model',
            'cli_flags': ['--reuse-model'],
            'description': 'Reuse identical generated models as the same ' 'type.',
            'required': False,
            'default': False,
            'multiple': False,
            'type': 'boolean',
            'choices': [],
        },
        {
            'name': 'enable_faux_immutability',
            'cli_flags': ['--enable-faux-immutability'],
            'description': 'Generate frozen Pydantic models so hashable field '
            'values make model instances hashable.',
            'required': False,
            'default': False,
            'multiple': False,
            'type': 'boolean',
            'choices': [],
        },
    ],
    'cli_examples': [
        {
            'options': ['--help'],
            'description': 'Show the CLI help message.',
            'cli_args': ['--help'],
            'input_schema': None,
        },
        {
            'options': ['--version'],
            'description': 'Show the installed fastapi-codegen version.',
            'cli_args': ['--version'],
            'input_schema': None,
        },
        {
            'options': ['--output'],
            'description': 'Directory where the generated FastAPI application '
            'is written.',
            'cli_args': [
                '--input',
                'openapi/default_template/simple.yaml',
                '--output',
                'app',
            ],
            'input_schema': 'openapi/default_template/simple.yaml',
        },
        {
            'options': ['--input'],
            'description': 'Generate a FastAPI application from an OpenAPI '
            'input file.',
            'cli_args': [
                '--input',
                'openapi/default_template/simple.yaml',
                '--output',
                'app',
            ],
            'input_schema': 'openapi/default_template/simple.yaml',
        },
        {
            'options': ['--template-dir'],
            'description': 'Render generated files with a custom template '
            'directory.',
            'cli_args': [
                '--input',
                'openapi/custom_template_security/custom_security.yaml',
                '--output',
                'app',
                '--template-dir',
                'custom_template/security',
            ],
            'input_schema': 'openapi/custom_template_security/custom_security.yaml',
        },
        {
            'options': ['--include-request-argument'],
            'description': 'Auto-inject a FastAPI Request argument in generated '
            'operation signatures when not present.',
            'cli_args': [
                '--input',
                'openapi/default_template/simple.yaml',
                '--output',
                'app',
                '--include-request-argument',
            ],
            'input_schema': 'openapi/default_template/simple.yaml',
        },
        {
            'options': ['--encoding'],
            'description': 'Read the input schema using an explicit text ' 'encoding.',
            'cli_args': [
                '--input',
                'openapi/default_template/simple.yaml',
                '--output',
                'app',
                '--encoding',
                'utf-16',
            ],
            'input_schema': 'openapi/default_template/simple.yaml',
        },
        {
            'options': ['--disable-timestamp'],
            'description': 'Omit the generated timestamp header from output ' 'files.',
            'cli_args': [
                '--input',
                'openapi/disable_timestamp/simple.yaml',
                '--output',
                'app',
                '--disable-timestamp',
            ],
            'input_schema': 'openapi/disable_timestamp/simple.yaml',
        },
        {
            'options': ['--strict-nullable'],
            'description': 'Respect explicit OpenAPI nullable flags when '
            'generating models.',
            'cli_args': [
                '--input',
                'openapi/default_template/nullable_test.yaml',
                '--output',
                'app',
                '--strict-nullable',
            ],
            'input_schema': 'openapi/default_template/nullable_test.yaml',
        },
        {
            'options': ['--generate-routers'],
            'description': 'Generate modular router files from tagged OpenAPI '
            'operations.',
            'cli_args': [
                '--input',
                'openapi/using_routers/using_routers_example.yaml',
                '--output',
                'app',
                '--template-dir',
                'modular_template',
                '--generate-routers',
            ],
            'input_schema': 'openapi/using_routers/using_routers_example.yaml',
        },
        {
            'options': ['--specify-tags'],
            'description': 'Generate or regenerate only the routers matching a '
            'comma-separated tag list.',
            'cli_args': [
                '--input',
                'openapi/using_routers/using_routers_example.yaml',
                '--output',
                'app',
                '--template-dir',
                'modular_template',
                '--generate-routers',
                '--specify-tags',
                'Wild Boars, Fat Cats',
            ],
            'input_schema': 'openapi/using_routers/using_routers_example.yaml',
        },
        {
            'options': ['--enum-field-as-literal'],
            'description': 'Render enum fields as Literal annotations.',
            'cli_args': [
                '--input',
                'openapi/default_template/duplicate_anonymus_parameter.yaml',
                '--output',
                'app',
                '--enum-field-as-literal',
                'all',
            ],
            'input_schema': 'openapi/default_template/duplicate_anonymus_parameter.yaml',
        },
        {
            'options': ['--use-annotated'],
            'description': 'Render model field constraints with ' 'typing.Annotated.',
            'cli_args': [
                '--input',
                'openapi/default_template/recursion.yaml',
                '--output',
                'app',
                '--use-annotated',
            ],
            'input_schema': 'openapi/default_template/recursion.yaml',
        },
        {
            'options': ['--enable-faux-immutability'],
            'description': 'Generate frozen Pydantic models so instances are '
            'hashable when their fields are hashable.',
            'cli_args': [
                '--input',
                'openapi/coverage/faux_immutability.yaml',
                '--output',
                'app',
                '--enable-faux-immutability',
            ],
            'input_schema': 'openapi/coverage/faux_immutability.yaml',
        },
        {
            'options': ['--model-file'],
            'description': 'Write generated models to a custom module path.',
            'cli_args': [
                '--input',
                'openapi/default_template/body_and_parameters.yaml',
                '--output',
                'app',
                '--model-file',
                'custom_models.py',
                '--model-template-dir',
                'model_templates',
                '--output-model-type',
                'pydantic_v2.BaseModel',
                '--python-version',
                '3.13',
            ],
            'input_schema': 'openapi/default_template/body_and_parameters.yaml',
        },
        {
            'options': ['--model-template-dir'],
            'description': 'Use a custom datamodel-code-generator template '
            'directory.',
            'cli_args': [
                '--input',
                'openapi/default_template/body_and_parameters.yaml',
                '--output',
                'app',
                '--model-file',
                'custom_models.py',
                '--model-template-dir',
                'model_templates',
                '--output-model-type',
                'pydantic_v2.BaseModel',
                '--python-version',
                '3.13',
            ],
            'input_schema': 'openapi/default_template/body_and_parameters.yaml',
        },
        {
            'options': ['--output-model-type'],
            'description': 'Choose the datamodel-code-generator output backend.',
            'cli_args': [
                '--input',
                'openapi/default_template/body_and_parameters.yaml',
                '--output',
                'app',
                '--model-file',
                'custom_models.py',
                '--model-template-dir',
                'model_templates',
                '--output-model-type',
                'pydantic_v2.BaseModel',
                '--python-version',
                '3.13',
            ],
            'input_schema': 'openapi/default_template/body_and_parameters.yaml',
        },
        {
            'options': ['--python-version'],
            'description': 'Target a specific Python version when formatting '
            'generated code.',
            'cli_args': [
                '--input',
                'openapi/default_template/body_and_parameters.yaml',
                '--output',
                'app',
                '--model-file',
                'custom_models.py',
                '--model-template-dir',
                'model_templates',
                '--output-model-type',
                'pydantic_v2.BaseModel',
                '--python-version',
                '3.13',
            ],
            'input_schema': 'openapi/default_template/body_and_parameters.yaml',
        },
        {
            'options': ['--reuse-model'],
            'description': 'Reuse generated model classes when another model '
            'has the same content.',
            'cli_args': [
                '--input',
                'openapi/default_template/reuse_model.yaml',
                '--output',
                'app',
                '--reuse-model',
            ],
            'input_schema': 'openapi/default_template/reuse_model.yaml',
        },
        {
            'options': ['--custom-visitor'],
            'description': 'Load a custom visitor module and expose additional '
            'template variables.',
            'cli_args': [
                '--input',
                'openapi/default_template/simple.yaml',
                '--output',
                'app',
                '--template-dir',
                'template',
                '--generate-routers',
                '--custom-visitor',
                'visitor.py',
            ],
            'input_schema': 'openapi/default_template/simple.yaml',
        },
    ],
    'schema_fixture_suites': [
        {
            'directory': 'default_template',
            'title': 'Default template',
            'notes': 'Core single-file generation scenarios exercised '
            'by the main CLI tests.',
        },
        {
            'directory': 'coverage',
            'title': 'Coverage fixtures',
            'notes': 'Focused fixtures for callbacks, non-200 '
            'responses, and other regression edges.',
        },
        {
            'directory': 'custom_template_security',
            'title': 'Custom template overrides',
            'notes': 'Template override coverage for ' '`--template-dir`.',
        },
        {
            'directory': 'disable_timestamp',
            'title': 'Timestamp suppression',
            'notes': 'Fixtures that exercise `--disable-timestamp`.',
        },
        {
            'directory': 'remote_ref',
            'title': 'Remote references',
            'notes': 'Fixtures whose `$ref` targets are resolved over '
            'HTTP at test time.',
        },
        {
            'directory': 'using_routers',
            'title': 'Router generation',
            'notes': 'Fixtures that exercise modular output and router '
            'regeneration.',
        },
    ],
    'schema_docs_preview': '# Supported Formats\n'
    '\n'
    'This page is generated from repository fixture inventory and '
    'config metadata.\n'
    'Run `tox run -e schema-docs` after changing supported inputs '
    'or model backends.\n'
    '\n'
    '## Input Formats\n'
    '\n'
    '| Format | Status | Evidence | Notes |\n'
    '|--------|--------|----------|-------|\n'
    '| OpenAPI YAML | tested | `tests/data/openapi/**/*.yaml` (27 '
    'fixtures) | Primary fixture format exercised under '
    '`tests/data/openapi/**/*.yaml`. |\n'
    '| OpenAPI JSON | tested | '
    '`tests/main/test_main.py::test_generate_from_json_input` | '
    'Covered by the JSON conversion CLI test in '
    '`tests/main/test_main.py`. |\n'
    '| Remote HTTP `$ref` targets | tested | '
    '`tests/main/test_main.py::test_generate_remote_ref` | Covered '
    'by the remote `$ref` generation test against a live HTTP '
    'server. |\n'
    '\n'
    '## Fixture Suites\n'
    '\n'
    '| Suite | Fixtures | Example files | Notes |\n'
    '|-------|----------|---------------|-------|\n'
    '| Default template | 19 | `body_and_parameters.yaml`, '
    '`content_in_parameters.yaml`, '
    '`content_in_parameters_inline.yaml` | Core single-file '
    'generation scenarios exercised by the main CLI tests. |\n'
    '| Coverage fixtures | 4 | `callbacks.yaml`, '
    '`callbacks_with_operation_id.yaml`, `faux_immutability.yaml` '
    '| Focused fixtures for callbacks, non-200 responses, and '
    'other regression edges. |\n'
    '| Custom template overrides | 1 | `custom_security.yaml` | '
    'Template override coverage for `--template-dir`. |\n'
    '| Timestamp suppression | 1 | `simple.yaml` | Fixtures that '
    'exercise `--disable-timestamp`. |\n'
    '| Remote references | 1 | `body_and_parameters.yaml` | '
    'Fixtures whose `$ref` targets are resolved over HTTP at test '
    'time. |\n'
    '| Router generation | 1 | `using_routers_example.yaml` | '
    'Fixtures that exercise modular output and router '
    'regeneration. |\n'
    '\n'
    '## Output Model Types\n'
    '\n'
    '| Output model type | Status | Notes |\n'
    '|-------------------|--------|-------|\n'
    '| `pydantic_v2.BaseModel` | supported | Pydantic v2 BaseModel '
    'output. |\n'
    '| `pydantic_v2.dataclass` | supported | Pydantic v2 dataclass '
    'output. |\n'
    '| `dataclasses.dataclass` | supported | Standard-library '
    'dataclass output. |\n'
    '| `typing.TypedDict` | supported | TypedDict-based model '
    'output. |\n'
    '| `msgspec.Struct` | supported | msgspec Struct output. |\n',
}
