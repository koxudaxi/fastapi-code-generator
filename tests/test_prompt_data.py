from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from scripts import build_prompt_data as prompt_data_module
from scripts.build_prompt_data import build_prompt_data


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
                        },
                        "option_description": "Generate a FastAPI application from an OpenAPI input file.",
                    },
                    {
                        "marker_kwargs": {
                            "options": ["--input"],
                        },
                        "option_description": "Generate a FastAPI application from an OpenAPI input file.\nExtra detail.",
                    },
                    {
                        "marker_kwargs": {
                            "options": ["--long"],
                        },
                        "option_description": "x" * 200,
                    },
                    {
                        "marker_kwargs": {
                            "options": ["--empty"],
                        },
                        "option_description": "",
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(prompt_data_module, "COLLECTION_PATH", collection_path)
    return collection_path


def test_build_prompt_data_generates_file(
    tmp_path: Path, cli_doc_collection: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert cli_doc_collection.exists()
    output_path = tmp_path / "prompt_data.py"
    monkeypatch.setattr(prompt_data_module, "OUTPUT_PATH", output_path)

    assert build_prompt_data(check=False) == 0

    content = output_path.read_text(encoding="utf-8")
    assert 'OPTION_DESCRIPTIONS: dict[str, str] = {' in content
    assert (
        '    "--input": "Generate a FastAPI application from an OpenAPI input file.",'
        in content
    )
    assert (
        '    "--output": "Generate a FastAPI application from an OpenAPI input file.",'
        in content
    )
    assert "--empty" not in content
    assert "..." in content


def test_build_prompt_data_missing_collection(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    collection_path = tmp_path / ".cli_doc_collection.json"
    output_path = tmp_path / "prompt_data.py"
    monkeypatch.setattr(prompt_data_module, "COLLECTION_PATH", collection_path)
    monkeypatch.setattr(prompt_data_module, "OUTPUT_PATH", output_path)

    assert build_prompt_data(check=False) == 1
    assert capsys.readouterr().err.splitlines() == [
        f"Collection file not found: {collection_path}",
        "Run: pytest --collect-cli-docs -p no:xdist",
    ]


def test_build_prompt_data_check_modes(
    tmp_path: Path,
    cli_doc_collection: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert cli_doc_collection.exists()
    output_path = tmp_path / "prompt_data.py"
    monkeypatch.setattr(prompt_data_module, "OUTPUT_PATH", output_path)

    assert build_prompt_data(check=True) == 1
    assert capsys.readouterr().err.strip() == f"Output file not found: {output_path}"

    output_path.write_text("stale\n", encoding="utf-8")
    assert build_prompt_data(check=True) == 1
    assert capsys.readouterr().err.strip() == f"Content mismatch: {output_path}"

    assert build_prompt_data(check=False) == 0
    assert build_prompt_data(check=True) == 0
    assert capsys.readouterr().out.splitlines()[-1] == f"OK: {output_path}"


def test_main_executes_cli_entrypoint(
    tmp_path: Path, cli_doc_collection: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert cli_doc_collection.exists()
    output_path = tmp_path / "prompt_data.py"
    monkeypatch.setattr(prompt_data_module, "OUTPUT_PATH", output_path)
    monkeypatch.setattr(sys, "argv", ["build_prompt_data.py"])

    assert prompt_data_module.main() == 0
    assert output_path.exists()

    monkeypatch.setattr(sys, "argv", ["build_prompt_data.py", "--check"])
    assert prompt_data_module.main() == 0
