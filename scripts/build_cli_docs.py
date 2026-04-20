"""Generate CLI reference documentation from collected pytest metadata."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

from click.testing import CliRunner
from typer.main import get_command

from fastapi_code_generator.__main__ import app

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_PATH = PROJECT_ROOT / "docs" / "cli-reference.md"
COLLECTION_PATH = PROJECT_ROOT / "tests" / "cli_doc" / ".cli_doc_collection.json"

ANSI_ESCAPE_PATTERN = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
BOX_DRAWING_TRANSLATION = str.maketrans(
    {
        "┌": "╭",
        "┐": "╮",
        "└": "╰",
        "┘": "╯",
    }
)


def _normalize_help_text(text: str) -> str:
    normalized = text.translate(BOX_DRAWING_TRANSLATION)
    return "\n".join(line.rstrip() for line in normalized.splitlines()).strip()


def get_help_text() -> str:
    """Return normalized CLI help output for the current environment."""
    env = os.environ.copy()
    env["COLUMNS"] = "94"
    env["TERMINAL_WIDTH"] = "94"
    env["LINES"] = "24"
    env["NO_COLOR"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    env["TERM"] = "dumb"
    completed = CliRunner(env=env).invoke(
        get_command(app),
        ["--help"],
        color=False,
        prog_name="fastapi-codegen",
    )
    if completed.exit_code != 0:
        msg = completed.stderr or completed.output or "failed to render CLI help"
        raise RuntimeError(msg)
    return _normalize_help_text(ANSI_ESCAPE_PATTERN.sub("", completed.output))


def load_cli_doc_collection() -> dict[str, object]:
    return json.loads(COLLECTION_PATH.read_text(encoding="utf-8"))


def render_examples(collection: dict[str, object]) -> str:
    sections: list[str] = []
    seen: set[str] = set()
    for item in collection.get("items", []):
        marker_kwargs = item.get("marker_kwargs", {})
        marker_key = json.dumps(marker_kwargs, sort_keys=True, ensure_ascii=False)
        if marker_key in seen:
            continue
        seen.add(marker_key)
        options = ", ".join(marker_kwargs.get("options", []))
        cli_args = " ".join(marker_kwargs.get("cli_args", []))
        input_schema = marker_kwargs.get("input_schema")
        related = marker_kwargs.get("related_options") or []
        lines = [
            f"### {options}",
            "",
            item.get("option_description", "").strip(),
            "",
            f"`fastapi-codegen {cli_args}`",
        ]
        if input_schema:
            lines.extend(["", f"Input schema: `{input_schema}`"])
        if related:
            related_options = ", ".join(f"`{option}`" for option in related)
            lines.extend(["", f"Related options: {related_options}"])
        sections.append("\n".join(lines).strip())
    return "\n\n".join(sections)


def render_document(help_text: str, collection: dict[str, object]) -> str:
    return f"""# CLI Reference

This page is generated from the current `fastapi-codegen --help` output.
Run `tox run -e cli-docs` after changing CLI options.

```text
{help_text}
```

## Tested CLI Scenarios

{render_examples(collection)}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check whether the generated CLI reference is up to date.",
    )
    args = parser.parse_args()

    rendered = render_document(get_help_text(), load_cli_doc_collection())
    existing = DOCS_PATH.read_text(encoding="utf-8") if DOCS_PATH.exists() else None

    if args.check:
        return 0 if existing == rendered else 1

    DOCS_PATH.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
