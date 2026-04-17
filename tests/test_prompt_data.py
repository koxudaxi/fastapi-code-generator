from __future__ import annotations

from pathlib import Path

from scripts.build_prompt_data import build_prompt_payload, update_prompt_data


def test_build_prompt_payload_contains_examples_and_config() -> None:
    payload = build_prompt_payload()

    assert payload["project"] == "fastapi-code-generator"
    assert payload["entrypoint"] == "fastapi-codegen"
    assert payload["config_options"]
    assert payload["cli_examples"]
    assert payload["schema_fixture_suites"]


def test_update_prompt_data_round_trip(tmp_path: Path) -> None:
    output_path = tmp_path / "prompt-data.json"

    assert update_prompt_data(output_path=output_path, check=False) == 0
    assert update_prompt_data(output_path=output_path, check=True) == 0
