"""Typed config metadata and generated type helpers for fastapi-code-generator."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Literal, TypedDict, cast, get_args, get_origin

from datamodel_code_generator import generate
from datamodel_code_generator.enums import DataModelType, InputFileType
from pydantic import BaseModel, ConfigDict, Field
from typer.main import get_command

EnumFieldAsLiteral = Literal["all", "one", "none"]
OutputModelTypeName = Literal[
    "pydantic_v2.BaseModel",
    "pydantic_v2.dataclass",
    "dataclasses.dataclass",
    "typing.TypedDict",
    "msgspec.Struct",
]
TargetPythonVersion = Literal["3.10", "3.11", "3.12", "3.13", "3.14"]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GENERATED_TYPES_PATH = (
    PROJECT_ROOT / "fastapi_code_generator" / "_types" / "generate_config_dict.py"
)
NON_CONFIG_COMMAND_PARAMS = {"version", "install_completion", "show_completion"}

INPUT_FORMAT_DESCRIPTIONS: dict[str, str] = {
    "yaml": "Primary fixture format exercised under `tests/data/openapi/**/*.yaml`.",
    "json": "Covered by the JSON conversion CLI test in `tests/main/test_main.py`.",
    "remote_ref": "Covered by the remote `$ref` generation test against a live HTTP server.",
}

OUTPUT_MODEL_TYPE_DESCRIPTIONS: dict[OutputModelTypeName, str] = {
    "pydantic_v2.BaseModel": "Pydantic v2 BaseModel output.",
    "pydantic_v2.dataclass": "Pydantic v2 dataclass output.",
    "dataclasses.dataclass": "Standard-library dataclass output.",
    "typing.TypedDict": "TypedDict-based model output.",
    "msgspec.Struct": "msgspec Struct output.",
}


@dataclass(frozen=True)
class ConfigOption:
    """Resolved CLI metadata for one generated config field."""

    name: str
    cli_flags: tuple[str, ...]
    description: str
    required: bool
    default: Any
    multiple: bool
    type_label: str
    choices: tuple[str, ...]


class CliOptionMetadata(TypedDict):
    """CLI metadata stored in `json_schema_extra`."""

    flags: list[str]
    multiple: bool


class CliFieldMetadata(TypedDict):
    """Wrapper for CLI metadata stored on config fields."""

    cli: CliOptionMetadata


def _cli_metadata(*flags: str, multiple: bool = False) -> CliFieldMetadata:
    return {"cli": {"flags": list(flags), "multiple": multiple}}


def _get_cli_metadata(field: Any) -> CliOptionMetadata:
    extra = field.json_schema_extra
    if not isinstance(extra, dict):
        return {"flags": [], "multiple": False}
    cli = extra.get("cli")
    if not isinstance(cli, dict):
        return {"flags": [], "multiple": False}
    flags = cli.get("flags")
    return {
        "flags": [str(flag) for flag in flags] if isinstance(flags, list) else [],
        "multiple": bool(cli.get("multiple", False)),
    }


class GenerateConfig(BaseModel):
    """Serializable generation settings that mirror the `fastapi-codegen` CLI."""

    model_config = ConfigDict(extra="forbid")

    encoding: str = Field(
        default="utf-8",
        description="Text encoding used to read the input OpenAPI document.",
        json_schema_extra=cast(Any, _cli_metadata("--encoding", "-e")),
    )
    input_file: str = Field(
        description="Path to the OpenAPI input document.",
        json_schema_extra=cast(Any, _cli_metadata("--input", "-i")),
    )
    output_dir: str = Field(
        description="Directory where the generated FastAPI application is written.",
        json_schema_extra=cast(Any, _cli_metadata("--output", "-o")),
    )
    model_file: str | None = Field(
        default=None,
        description="Optional output path for the generated model module.",
        json_schema_extra=cast(Any, _cli_metadata("--model-file", "-m")),
    )
    template_dir: str | None = Field(
        default=None,
        description="Optional custom template directory for application files.",
        json_schema_extra=cast(Any, _cli_metadata("--template-dir", "-t")),
    )
    model_template_dir: str | None = Field(
        default=None,
        description="Optional custom datamodel-code-generator template directory.",
        json_schema_extra=cast(Any, _cli_metadata("--model-template-dir")),
    )
    enum_field_as_literal: EnumFieldAsLiteral | None = Field(
        default=None,
        description="Render enum-like values as Literal annotations.",
        json_schema_extra=cast(Any, _cli_metadata("--enum-field-as-literal")),
    )
    generate_routers: bool = Field(
        default=False,
        description="Generate router modules with the modular template.",
        json_schema_extra=cast(Any, _cli_metadata("--generate-routers", "-r")),
    )
    specify_tags: str | None = Field(
        default=None,
        description="Comma-separated router tags to regenerate with modular output.",
        json_schema_extra=cast(Any, _cli_metadata("--specify-tags")),
    )
    custom_visitors: list[str] | None = Field(
        default=None,
        description="Additional visitor module paths that inject template variables.",
        json_schema_extra=cast(
            Any, _cli_metadata("--custom-visitor", "-c", multiple=True)
        ),
    )
    disable_timestamp: bool = Field(
        default=False,
        description="Omit timestamp headers from generated files.",
        json_schema_extra=cast(Any, _cli_metadata("--disable-timestamp")),
    )
    output_model_type: OutputModelTypeName = Field(
        default="pydantic_v2.BaseModel",
        description="Model backend passed through to datamodel-code-generator.",
        json_schema_extra=cast(Any, _cli_metadata("--output-model-type", "-d")),
    )
    python_version: TargetPythonVersion = Field(
        default="3.10",
        description="Target Python version used when formatting generated code.",
        json_schema_extra=cast(Any, _cli_metadata("--python-version", "-p")),
    )
    use_annotated: bool = Field(
        default=False,
        description="Use `typing.Annotated` for generated model field constraints.",
        json_schema_extra=cast(Any, _cli_metadata("--use-annotated")),
    )


def _type_label(annotation: Any) -> str:
    if annotation is type(None):
        return "null"
    if annotation is str:
        return "string"
    if annotation is bool:
        return "boolean"
    if annotation is int:
        return "integer"
    origin = get_origin(annotation)
    if origin is Literal:
        return "literal"
    if origin is list:
        (item_type,) = get_args(annotation)
        return f"list[{_type_label(item_type)}]"
    if origin is not None:
        args = [arg for arg in get_args(annotation) if arg is not type(None)]
        nullable = len(args) != len(get_args(annotation))
        if len(args) == 1:
            label = _type_label(args[0])
        else:
            label = " | ".join(_type_label(arg) for arg in args)
        return f"{label} | null" if nullable else label
    return getattr(annotation, "__name__", repr(annotation))


def _literal_choices(annotation: Any) -> tuple[str, ...]:
    origin = get_origin(annotation)
    if origin is Literal:
        return tuple(str(value) for value in get_args(annotation))
    if origin is list:
        (item_type,) = get_args(annotation)
        return _literal_choices(item_type)
    if origin is not None:
        values: list[str] = []
        for arg in get_args(annotation):
            values.extend(_literal_choices(arg))
        return tuple(dict.fromkeys(values))
    return ()


def _normalize_default(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, list):
        return [_normalize_default(item) for item in value]
    return value


def get_command_config_params() -> dict[str, Any]:
    """Return the actionable CLI params that should map to `GenerateConfig`."""
    from fastapi_code_generator.cli import app

    command = get_command(app)
    return {
        param.name: param
        for param in command.params
        if param.name is not None and param.name not in NON_CONFIG_COMMAND_PARAMS
    }


def iter_config_options() -> tuple[ConfigOption, ...]:
    """Return config field metadata after validating it against the real CLI."""

    validate_generate_config_model()
    options: list[ConfigOption] = []
    for name, field in GenerateConfig.model_fields.items():
        cli = _get_cli_metadata(field)
        options.append(
            ConfigOption(
                name=name,
                cli_flags=tuple(cli["flags"]),
                description=field.description or "",
                required=field.is_required(),
                default=(
                    None if field.is_required() else _normalize_default(field.default)
                ),
                multiple=cli["multiple"],
                type_label=_type_label(field.annotation),
                choices=_literal_choices(field.annotation),
            )
        )
    return tuple(options)


def validate_generate_config_model() -> None:
    """Raise if the typed config model drifts away from the Typer CLI."""

    params = get_command_config_params()
    field_names = tuple(GenerateConfig.model_fields)
    param_names = tuple(params)
    if field_names != param_names:
        raise ValueError(
            "GenerateConfig fields do not match CLI params: "
            f"{field_names!r} != {param_names!r}"
        )

    for name, field in GenerateConfig.model_fields.items():
        cli = _get_cli_metadata(field)
        param = params[name]
        expected_flags = tuple(cli["flags"])
        if tuple(param.opts) != expected_flags:
            raise ValueError(
                f"{name} flags drifted: expected {expected_flags!r}, got {tuple(param.opts)!r}"
            )
        if cli["multiple"] != bool(getattr(param, "multiple", False)):
            raise ValueError(f"{name} multiple setting drifted from the CLI")
        if field.is_required() != bool(param.required):
            raise ValueError(f"{name} required flag drifted from the CLI")
        if not field.is_required():
            expected_default = _normalize_default(field.default)
            actual_default = _normalize_default(param.default)
            if expected_default != actual_default:
                raise ValueError(
                    f"{name} default drifted: expected {expected_default!r}, got {actual_default!r}"
                )
        expected_choices = _literal_choices(field.annotation)
        actual_choices = tuple(getattr(param.type, "choices", ()) or ())
        if expected_choices != actual_choices:
            raise ValueError(
                f"{name} choices drifted: expected {expected_choices!r}, got {actual_choices!r}"
            )


def build_generate_config_typed_dict() -> str:
    """Render `GenerateConfig` as a generated TypedDict module."""

    validate_generate_config_model()
    schema = json.dumps(GenerateConfig.model_json_schema(), sort_keys=True)
    with TemporaryDirectory() as tmp_dir:
        output_path = Path(tmp_dir) / "generate_config_dict.py"
        generate(
            schema,
            input_filename="fastapi_code_generator/config.py",
            input_file_type=InputFileType.JsonSchema,
            output=output_path,
            output_model_type=DataModelType.TypingTypedDict,
            class_name="GenerateConfigDict",
            disable_timestamp=True,
            use_standard_collections=True,
        )
        content = output_path.read_text(encoding="utf-8")
        return content.replace("(TypedDict, closed=True)", "(TypedDict)")


def update_generated_types(
    *, check: bool = False, output_path: Path = GENERATED_TYPES_PATH
) -> int:
    """Write or validate the generated config TypedDict module."""

    content = build_generate_config_typed_dict()
    existing = output_path.read_text(encoding="utf-8") if output_path.exists() else None
    if check:
        return 0 if existing == content else 1
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if existing != content:
        output_path.write_text(content, encoding="utf-8")
    return 0


def main() -> int:
    """Run the config-types generator."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        default=GENERATED_TYPES_PATH,
        help="Target path for the generated TypedDict module.",
    )
    args = parser.parse_args()
    return update_generated_types(check=args.check, output_path=args.output)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
