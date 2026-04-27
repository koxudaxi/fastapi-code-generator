from __future__ import annotations

import re
from pathlib import Path

from typer.main import get_command

from fastapi_code_generator.__main__ import app
from scripts.build_cli_docs import get_help_text

README_PATH = Path(__file__).resolve().parent.parent / "README.md"
START_MARK = "<!-- start command help -->"
END_MARK = "<!-- end command help -->"


def _extract_help_snapshot(readme_text: str) -> str:
    start = readme_text.index(START_MARK) + len(START_MARK)
    end = readme_text.index(END_MARK)
    return (
        readme_text[start:end]
        .strip()
        .removeprefix("```text")
        .removesuffix("```")
        .strip()
    )


def test_readme_help_snapshot_matches_cli() -> None:
    readme_text = README_PATH.read_text(encoding="utf-8")
    assert _extract_help_snapshot(readme_text) == get_help_text()


def test_readme_cli_options_exist() -> None:
    readme_text = README_PATH.read_text(encoding="utf-8")
    referenced = set(re.findall(r"--[a-z0-9-]+", readme_text))
    command = get_command(app)
    known = {
        option
        for param in command.params
        for option in [
            *getattr(param, "opts", []),
            *getattr(param, "secondary_opts", []),
        ]
        if option.startswith("--")
    }
    assert referenced <= (known | {"--help"})
