from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypedDict, cast

import pytest
import time_machine
from inline_snapshot import external_file, register_format_alias
from typing_extensions import Required

CLI_DOC_COLLECTION_OUTPUT = (
    Path(__file__).parent / "cli_doc" / ".cli_doc_collection.json"
)
CLI_DOC_SCHEMA_VERSION = 1


class CliDocKwargs(TypedDict, total=False):
    options: Required[list[str]]
    option_description: Required[str]
    cli_args: Required[list[str]]
    input_schema: str | None
    golden_output: str | None
    expected_stdout: str | None
    related_options: list[str] | None
    aliases: list[str] | None


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--collect-cli-docs",
        action="store_true",
        default=False,
        help="Collect CLI documentation metadata from tests marked with @pytest.mark.cli_doc",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "cli_doc(options, option_description, cli_args, input_schema=None, golden_output=None, "
        "expected_stdout=None, related_options=None, aliases=None): "
        "Mark test as CLI documentation source.",
    )
    config._cli_doc_items = []


def pytest_collection_modifyitems(
    session: pytest.Session,
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    del session
    for item in items:
        marker = item.get_closest_marker("cli_doc")
        if marker is None:
            continue
        kwargs = cast("CliDocKwargs", marker.kwargs)
        config._cli_doc_items.append(
            {
                "node_id": item.nodeid,
                "marker_kwargs": kwargs,
                "option_description": kwargs.get("option_description", ""),
            }
        )


def pytest_runtestloop(session: pytest.Session) -> bool | None:  # pragma: no cover
    if session.config.getoption("--collect-cli-docs"):
        return True
    return None


def pytest_sessionfinish(
    session: pytest.Session, exitstatus: int
) -> None:  # pragma: no cover
    del exitstatus
    config = session.config
    if not config.getoption("--collect-cli-docs"):
        return
    output = {
        "schema_version": CLI_DOC_SCHEMA_VERSION,
        "items": getattr(config, "_cli_doc_items", []),
    }
    CLI_DOC_COLLECTION_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    CLI_DOC_COLLECTION_OUTPUT.write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _parse_time_string(time_str: str) -> datetime:
    for fmt in (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(time_str, fmt)
        except ValueError:
            continue
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    return datetime.fromisoformat(time_str.replace("Z", "+00:00"))


def freeze_time(time_to_freeze: str, **kwargs: Any) -> time_machine.travel:
    del kwargs
    return time_machine.travel(_parse_time_string(time_to_freeze), tick=False)


def _normalize_line_endings(text: str) -> str:
    return text.replace("\r\n", "\n")


def _assert_with_external_file(content: str, expected_path: Path) -> None:
    expected = external_file(expected_path)
    normalized_content = _normalize_line_endings(content)
    if isinstance(expected, str):
        assert normalized_content == _normalize_line_endings(expected)
    else:  # pragma: no cover
        assert normalized_content == _normalize_line_endings(expected._load_value())


def assert_directory_content(output_dir: Path, expected_dir: Path) -> None:
    output_files = sorted(
        path.relative_to(output_dir) for path in output_dir.rglob("*") if path.is_file()
    )
    expected_files = sorted(
        path.relative_to(expected_dir)
        for path in expected_dir.rglob("*")
        if path.is_file()
    )
    assert output_files == expected_files
    for relative_path in output_files:
        _assert_with_external_file(
            output_dir.joinpath(relative_path).read_text(encoding="utf-8"),
            expected_dir.joinpath(relative_path),
        )


def validate_generated_code(output_path: Path) -> None:
    targets = (
        [output_path] if output_path.is_file() else sorted(output_path.rglob("*.py"))
    )
    for target in targets:
        compile(target.read_text(encoding="utf-8"), str(target), "exec")


@pytest.fixture(autouse=True)
def _inline_snapshot_file_formats() -> None:
    register_format_alias(".py", ".txt")
    register_format_alias(".pyi", ".txt")
