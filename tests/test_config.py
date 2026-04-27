from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Literal

import pytest

from fastapi_code_generator import config as config_module
from fastapi_code_generator.config import (
    GENERATED_TYPES_PATH,
    GenerateConfig,
    _get_cli_metadata,
    _literal_choices,
    _normalize_default,
    _type_label,
    build_generate_config_typed_dict,
    get_command_config_params,
    iter_config_options,
    update_generated_types,
    validate_generate_config_model,
)


def test_generate_config_defaults() -> None:
    config = GenerateConfig(input_file="api.yaml", output_dir="app")

    assert config.encoding == "utf-8"
    assert config.output_model_type == "pydantic_v2.BaseModel"
    assert config.python_version == "3.10"
    assert config.custom_visitors is None
    assert config.generate_routers is False


def test_validate_generate_config_model_matches_cli() -> None:
    validate_generate_config_model()


def test_iter_config_options_exposes_real_cli_metadata() -> None:
    options = {option.name: option for option in iter_config_options()}

    assert options["input_file"].cli_flags == ("--input", "-i")
    assert options["input_file"].required is True
    assert options["output_dir"].cli_flags == ("--output", "-o")
    assert options["custom_visitors"].multiple is True
    assert options["output_model_type"].choices == (
        "pydantic_v2.BaseModel",
        "pydantic_v2.dataclass",
        "dataclasses.dataclass",
        "typing.TypedDict",
        "msgspec.Struct",
    )


def test_generated_config_typed_dict_is_up_to_date() -> None:
    assert (
        GENERATED_TYPES_PATH.read_text(encoding="utf-8")
        == build_generate_config_typed_dict()
    )


def test_config_helper_functions_cover_branching() -> None:
    assert _type_label(type(None)) == "null"
    assert _type_label(Literal["a", "b"]) == "literal"
    assert _type_label(list[Literal["a"]]) == "list[literal]"
    assert _type_label(str | None) == "string | null"
    assert _type_label(int | str | None) == "integer | string | null"
    assert _type_label(bool) == "boolean"
    assert _type_label(int) == "integer"
    assert _type_label(Path) == "Path"
    assert _literal_choices(Literal["a", "b"]) == ("a", "b")
    assert _literal_choices(list[Literal["a"]]) == ("a",)
    assert _literal_choices(str | None) == ()
    assert _normalize_default(Path("out.py")) == "out.py"
    assert _normalize_default([Path("out.py"), "raw"]) == ["out.py", "raw"]
    assert _get_cli_metadata(SimpleNamespace(json_schema_extra=None)) == {
        "flags": [],
        "multiple": False,
    }
    assert _get_cli_metadata(SimpleNamespace(json_schema_extra={"cli": "broken"})) == {
        "flags": [],
        "multiple": False,
    }
    assert _get_cli_metadata(
        SimpleNamespace(json_schema_extra={"cli": {"flags": "--broken", "multiple": 1}})
    ) == {"flags": [], "multiple": True}


def _fake_params() -> dict[str, SimpleNamespace]:
    fake: dict[str, SimpleNamespace] = {}
    for name, param in get_command_config_params().items():
        fake[name] = SimpleNamespace(
            opts=tuple(param.opts),
            multiple=bool(getattr(param, "multiple", False)),
            required=bool(param.required),
            default=param.default,
            type=SimpleNamespace(
                choices=tuple(getattr(param.type, "choices", ()) or ())
            ),
        )
    return fake


def test_validate_generate_config_model_detects_name_drift(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(config_module, "get_command_config_params", lambda: {})
    with pytest.raises(ValueError, match="fields do not match CLI params"):
        validate_generate_config_model()


def test_validate_generate_config_model_detects_flag_drift(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = _fake_params()
    fake["encoding"].opts = ("--broken",)
    monkeypatch.setattr(config_module, "get_command_config_params", lambda: fake)
    with pytest.raises(ValueError, match="flags drifted"):
        validate_generate_config_model()


def test_validate_generate_config_model_detects_multiple_drift(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = _fake_params()
    fake["custom_visitors"].multiple = False
    monkeypatch.setattr(config_module, "get_command_config_params", lambda: fake)
    with pytest.raises(ValueError, match="multiple setting drifted"):
        validate_generate_config_model()


def test_validate_generate_config_model_detects_required_drift(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = _fake_params()
    fake["input_file"].required = False
    monkeypatch.setattr(config_module, "get_command_config_params", lambda: fake)
    with pytest.raises(ValueError, match="required flag drifted"):
        validate_generate_config_model()


def test_validate_generate_config_model_detects_default_drift(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = _fake_params()
    fake["encoding"].default = "latin-1"
    monkeypatch.setattr(config_module, "get_command_config_params", lambda: fake)
    with pytest.raises(ValueError, match="default drifted"):
        validate_generate_config_model()


def test_validate_generate_config_model_detects_choice_drift(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = _fake_params()
    fake["output_model_type"].type = SimpleNamespace(choices=("broken",))
    monkeypatch.setattr(config_module, "get_command_config_params", lambda: fake)
    with pytest.raises(ValueError, match="choices drifted"):
        validate_generate_config_model()


def test_update_generated_types_round_trip(tmp_path: Path) -> None:
    output_path = tmp_path / "generate_config_dict.py"
    assert update_generated_types(output_path=output_path, check=False) == 0
    assert update_generated_types(output_path=output_path, check=False) == 0
    assert update_generated_types(output_path=output_path, check=True) == 0


def test_config_main_accepts_custom_output(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    output_path = tmp_path / "generate_config_dict.py"
    monkeypatch.setattr(sys, "argv", ["config.py", "--output", str(output_path)])
    assert config_module.main() == 0
    monkeypatch.setattr(
        sys, "argv", ["config.py", "--check", "--output", str(output_path)]
    )
    assert config_module.main() == 0
