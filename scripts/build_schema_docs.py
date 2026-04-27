"""Generate repository-backed schema support documentation."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from fastapi_code_generator.config import (
    INPUT_FORMAT_DESCRIPTIONS,
    OUTPUT_MODEL_TYPE_DESCRIPTIONS,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_PATH = PROJECT_ROOT / "docs" / "supported_formats.md"
OPENAPI_FIXTURES_ROOT = PROJECT_ROOT / "tests" / "data" / "openapi"


@dataclass(frozen=True)
class FixtureSuite:
    """One tested fixture family under `tests/data/openapi`."""

    directory: str
    title: str
    notes: str


FIXTURE_SUITES: tuple[FixtureSuite, ...] = (
    FixtureSuite(
        directory="default_template",
        title="Default template",
        notes="Core single-file generation scenarios exercised by the main CLI tests.",
    ),
    FixtureSuite(
        directory="coverage",
        title="Coverage fixtures",
        notes="Focused fixtures for callbacks, non-200 responses, and other regression edges.",
    ),
    FixtureSuite(
        directory="custom_template_security",
        title="Custom template overrides",
        notes="Template override coverage for `--template-dir`.",
    ),
    FixtureSuite(
        directory="disable_timestamp",
        title="Timestamp suppression",
        notes="Fixtures that exercise `--disable-timestamp`.",
    ),
    FixtureSuite(
        directory="remote_ref",
        title="Remote references",
        notes="Fixtures whose `$ref` targets are resolved over HTTP at test time.",
    ),
    FixtureSuite(
        directory="using_routers",
        title="Router generation",
        notes="Fixtures that exercise modular output and router regeneration.",
    ),
)


def _count_yaml_fixtures() -> int:
    return len(tuple(OPENAPI_FIXTURES_ROOT.rglob("*.yaml")))


def _render_input_formats() -> str:
    rows = [
        "| Format | Status | Evidence | Notes |",
        "|--------|--------|----------|-------|",
        (
            f"| OpenAPI YAML | tested | `tests/data/openapi/**/*.yaml` "
            f"({_count_yaml_fixtures()} fixtures) | {INPUT_FORMAT_DESCRIPTIONS['yaml']} |"
        ),
        (
            "| OpenAPI JSON | tested | "
            "`tests/main/test_main.py::test_generate_from_json_input` | "
            f"{INPUT_FORMAT_DESCRIPTIONS['json']} |"
        ),
        (
            "| Remote HTTP `$ref` targets | tested | "
            "`tests/main/test_main.py::test_generate_remote_ref` | "
            f"{INPUT_FORMAT_DESCRIPTIONS['remote_ref']} |"
        ),
    ]
    return "\n".join(rows)


def _suite_fixture_paths(directory: str) -> tuple[Path, ...]:
    return tuple(sorted((OPENAPI_FIXTURES_ROOT / directory).glob("*.yaml")))


def _render_fixture_suites() -> str:
    rows = [
        "| Suite | Fixtures | Example files | Notes |",
        "|-------|----------|---------------|-------|",
    ]
    for suite in FIXTURE_SUITES:
        fixtures = _suite_fixture_paths(suite.directory)
        example_files = ", ".join(f"`{path.name}`" for path in fixtures[:3])
        rows.append(
            f"| {suite.title} | {len(fixtures)} | {example_files} | {suite.notes} |"
        )
    return "\n".join(rows)


def _render_output_model_types() -> str:
    rows = [
        "| Output model type | Status | Notes |",
        "|-------------------|--------|-------|",
    ]
    for value, description in OUTPUT_MODEL_TYPE_DESCRIPTIONS.items():
        rows.append(f"| `{value}` | supported | {description} |")
    return "\n".join(rows)


def render_document() -> str:
    """Render `docs/supported_formats.md`."""

    return """# Supported Formats

This page is generated from repository fixture inventory and config metadata.
Run `tox run -e schema-docs` after changing supported inputs or model backends.

## Input Formats

{input_formats}

## Fixture Suites

{fixture_suites}

## Output Model Types

{output_model_types}
""".format(
        input_formats=_render_input_formats(),
        fixture_suites=_render_fixture_suites(),
        output_model_types=_render_output_model_types(),
    )


def update_docs(*, check: bool) -> int:
    """Write or validate the supported formats document."""

    rendered = render_document()
    existing = DOCS_PATH.read_text(encoding="utf-8") if DOCS_PATH.exists() else None
    if check:
        return 0 if existing == rendered else 1
    if existing != rendered:
        DOCS_PATH.write_text(rendered, encoding="utf-8")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return update_docs(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
