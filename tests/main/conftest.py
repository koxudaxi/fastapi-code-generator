from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from fastapi_code_generator.__main__ import main
from tests.conftest import assert_directory_content, validate_generated_code

if TYPE_CHECKING:
    from collections.abc import Sequence

DATA_PATH = Path(__file__).parent.parent / "data"
EXPECTED_PATH = DATA_PATH / "expected"
EXPECTED_OPENAPI_PATH = EXPECTED_PATH / "openapi"


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    return tmp_path / "generated"


def run_main_with_args(args: Sequence[str]) -> int:
    return main(list(args))


def run_cli_and_assert(
    *,
    input_path: Path,
    output_path: Path,
    expected_path: Path,
    extra_args: Sequence[str] | None = None,
) -> None:
    args = [
        "--input",
        str(input_path),
        "--output",
        str(output_path),
    ]
    if extra_args is not None:
        args.extend(extra_args)
    assert run_main_with_args(args) == 0
    assert_directory_content(output_path, expected_path)
    validate_generated_code(output_path)
