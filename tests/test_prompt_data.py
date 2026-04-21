from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts import build_cli_docs as cli_docs_module
from scripts.build_prompt_data import build_prompt_payload, update_prompt_data


@pytest.fixture
def cli_doc_collection(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    collection_path = tmp_path / ".cli_doc_collection.json"
    collection_path.write_text(
        json.dumps(
            {
                "items": [
                    {
                        "marker_kwargs": {
                            "options": ["--input", "--output"],
                            "cli_args": ["--input", "api.yaml", "--output", "app"],
                            "input_schema": "simple.yaml",
                        },
                        "option_description": "Generate a FastAPI application from an OpenAPI input file.",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(cli_docs_module, "COLLECTION_PATH", collection_path)
    return collection_path


def test_build_prompt_payload_contains_examples_and_config(
    cli_doc_collection: Path,
) -> None:
    assert cli_doc_collection.exists()
    payload = build_prompt_payload()

    assert payload["project"] == "fastapi-code-generator"
    assert payload["entrypoint"] == "fastapi-codegen"
    assert payload["config_options"]
    assert payload["cli_examples"]
    assert payload["schema_fixture_suites"]


def test_update_prompt_data_round_trip(
    tmp_path: Path, cli_doc_collection: Path
) -> None:
    assert cli_doc_collection.exists()
    output_path = tmp_path / "prompt-data.json"

    assert update_prompt_data(output_path=output_path, check=False) == 0
    assert update_prompt_data(output_path=output_path, check=True) == 0
