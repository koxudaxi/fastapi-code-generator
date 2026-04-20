"""Build prompt-oriented JSON data from the repo's generated metadata."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi_code_generator.config import iter_config_options
from scripts.build_cli_docs import load_cli_doc_collection
from scripts.build_schema_docs import FIXTURE_SUITES, render_document as render_schema_docs


def build_prompt_payload() -> dict[str, object]:
    """Return a machine-readable bundle for downstream prompt tooling."""

    try:
        collection = load_cli_doc_collection()
    except FileNotFoundError:
        print("Warning: cli doc collection is missing; prompt examples will be empty.", file=sys.stderr)
        collection = {"items": []}
    examples: list[dict[str, object]] = []
    seen: set[str] = set()
    for item in collection.get("items", []):
        marker_kwargs = item.get("marker_kwargs", {})
        key = json.dumps(marker_kwargs, sort_keys=True, ensure_ascii=False)
        if key in seen:
            continue
        seen.add(key)
        examples.append(
            {
                "options": marker_kwargs.get("options", []),
                "description": item.get("option_description", ""),
                "cli_args": marker_kwargs.get("cli_args", []),
                "input_schema": marker_kwargs.get("input_schema"),
            }
        )

    return {
        "project": "fastapi-code-generator",
        "entrypoint": "fastapi-codegen",
        "config_options": [
            {
                "name": option.name,
                "cli_flags": list(option.cli_flags),
                "description": option.description,
                "required": option.required,
                "default": option.default,
                "multiple": option.multiple,
                "type": option.type_label,
                "choices": list(option.choices),
            }
            for option in iter_config_options()
        ],
        "cli_examples": examples,
        "schema_fixture_suites": [
            {
                "directory": suite.directory,
                "title": suite.title,
                "notes": suite.notes,
            }
            for suite in FIXTURE_SUITES
        ],
        "schema_docs_preview": render_schema_docs(),
    }


def update_prompt_data(*, output_path: Path | None, check: bool) -> int:
    payload = json.dumps(build_prompt_payload(), indent=2, ensure_ascii=False) + "\n"
    if output_path is None:
        if check:
            print("--check requires --output", file=sys.stderr)
            return 1
        sys.stdout.write(payload)
        return 0

    existing = output_path.read_text(encoding="utf-8") if output_path.exists() else None
    if check:
        return 0 if existing == payload else 1
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if existing != payload:
        output_path.write_text(payload, encoding="utf-8")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write the generated JSON payload.",
    )
    args = parser.parse_args()
    return update_prompt_data(output_path=args.output, check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
