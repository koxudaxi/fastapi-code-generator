# Supported Formats

This page is generated from repository fixture inventory and config metadata.
Run `tox run -e schema-docs` after changing supported inputs or model backends.

## Input Formats

| Format | Status | Evidence | Notes |
|--------|--------|----------|-------|
| OpenAPI YAML | tested | `tests/data/openapi/**/*.yaml` (25 fixtures) | Primary fixture format exercised under `tests/data/openapi/**/*.yaml`. |
| OpenAPI JSON | tested | `tests/main/test_main.py::test_generate_from_json_input` | Covered by the JSON conversion CLI test in `tests/main/test_main.py`. |
| Remote HTTP `$ref` targets | tested | `tests/main/test_main.py::test_generate_remote_ref` | Covered by the remote `$ref` generation test against a live HTTP server. |

## Fixture Suites

| Suite | Fixtures | Example files | Notes |
|-------|----------|---------------|-------|
| Default template | 18 | `body_and_parameters.yaml`, `content_in_parameters.yaml`, `content_in_parameters_inline.yaml` | Core single-file generation scenarios exercised by the main CLI tests. |
| Coverage fixtures | 3 | `callbacks.yaml`, `callbacks_with_operation_id.yaml`, `non_200_responses.yaml` | Focused fixtures for callbacks, non-200 responses, and other regression edges. |
| Custom template overrides | 1 | `custom_security.yaml` | Template override coverage for `--template-dir`. |
| Timestamp suppression | 1 | `simple.yaml` | Fixtures that exercise `--disable-timestamp`. |
| Remote references | 1 | `body_and_parameters.yaml` | Fixtures whose `$ref` targets are resolved over HTTP at test time. |
| Router generation | 1 | `using_routers_example.yaml` | Fixtures that exercise modular output and router regeneration. |

## Output Model Types

| Output model type | Status | Notes |
|-------------------|--------|-------|
| `pydantic_v2.BaseModel` | supported | Pydantic v2 BaseModel output. |
| `pydantic_v2.dataclass` | supported | Pydantic v2 dataclass output. |
| `dataclasses.dataclass` | supported | Standard-library dataclass output. |
| `typing.TypedDict` | supported | TypedDict-based model output. |
| `msgspec.Struct` | supported | msgspec Struct output. |
