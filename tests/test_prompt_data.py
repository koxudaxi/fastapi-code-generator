from __future__ import annotations

import json
import runpy
import sys
from pathlib import Path

import pytest

from scripts import build_cli_docs as cli_docs_module
from scripts import build_prompt_data as prompt_data_module
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
    assert update_prompt_data(output_path=output_path, check=False) == 0


def test_build_prompt_payload_handles_missing_collection(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        prompt_data_module,
        "load_cli_doc_collection",
        lambda: (_ for _ in ()).throw(FileNotFoundError),
    )

    payload = build_prompt_payload()

    assert payload["cli_examples"] == []
    assert (
        capsys.readouterr().err.strip()
        == "Warning: cli doc collection is missing; prompt examples will be empty."
    )


def test_build_prompt_payload_deduplicates_examples(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        prompt_data_module,
        "load_cli_doc_collection",
        lambda: {
            "items": [
                {
                    "marker_kwargs": {
                        "options": ["--input", "--output"],
                        "cli_args": ["--input", "api.yaml", "--output", "app"],
                        "input_schema": "simple.yaml",
                    },
                    "option_description": "Generate app.",
                },
                {
                    "marker_kwargs": {
                        "options": ["--input", "--output"],
                        "cli_args": ["--input", "api.yaml", "--output", "app"],
                        "input_schema": "simple.yaml",
                    },
                    "option_description": "Generate app.",
                },
            ]
        },
    )

    payload = build_prompt_payload()

    assert len(payload["cli_examples"]) == 1


def test_update_prompt_data_supports_python_output_and_stdout(
    tmp_path: Path,
    cli_doc_collection: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert cli_doc_collection.exists()
    output_path = tmp_path / "prompt_data.py"

    assert update_prompt_data(output_path=output_path, check=False) == 0
    assert "PROMPT_DATA: dict[str, Any] =" in output_path.read_text(encoding="utf-8")

    assert update_prompt_data(output_path=None, check=False) == 0
    assert '"project": "fastapi-code-generator"' in capsys.readouterr().out


def test_update_prompt_data_requires_output_for_check(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert update_prompt_data(output_path=None, check=True) == 1
    assert capsys.readouterr().err.strip() == "--check requires --output"


def test_main_executes_cli_entrypoint(
    tmp_path: Path, cli_doc_collection: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert cli_doc_collection.exists()
    output_path = tmp_path / "prompt-data.json"
    script_path = Path(prompt_data_module.__file__)
    project_root = str(script_path.resolve().parent.parent)
    monkeypatch.setattr(
        sys, "path", [path for path in sys.path if path != project_root]
    )

    monkeypatch.setattr(
        sys,
        "argv",
        ["build_prompt_data.py", "--output", str(output_path)],
    )
    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path(str(script_path), run_name="__main__")

    assert exc_info.value.code == 0

    monkeypatch.setattr(
        sys,
        "argv",
        ["build_prompt_data.py", "--check", "--output", str(output_path)],
    )
    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path(str(script_path), run_name="__main__")

    assert exc_info.value.code == 0
