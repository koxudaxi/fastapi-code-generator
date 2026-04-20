"""Update CLI help snapshots in markdown documentation files."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

START_MARK = "<!-- start command help -->"
END_MARK = "<!-- end command help -->"
CODE_BLOCK_START = "```text"
CODE_BLOCK_END = "```"

PROJECT_DIR = Path(__file__).resolve().parent.parent
TARGET_MARKDOWN_FILES = [
    PROJECT_DIR / "README.md",
    PROJECT_DIR / "docs" / "index.md",
]

ANSI_ESCAPE_PATTERN = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def _normalize_help_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


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
    completed = subprocess.run(
        [sys.executable, "-m", "fastapi_code_generator", "--help"],
        check=True,
        capture_output=True,
        encoding="utf-8",
        text=True,
        cwd=PROJECT_DIR,
        env=env,
    )
    return _normalize_help_text(ANSI_ESCAPE_PATTERN.sub("", completed.stdout))


def inject_help(markdown_text: str, help_text: str) -> str:
    """Inject help text into markdown between start and end markers."""
    start_pos = markdown_text.find(START_MARK)
    end_pos = markdown_text.find(END_MARK)
    if start_pos == -1 or end_pos == -1:
        msg = f"Could not find {START_MARK} or {END_MARK}"
        raise ValueError(msg)
    return (
        markdown_text[: start_pos + len(START_MARK)]
        + "\n"
        + CODE_BLOCK_START
        + "\n"
        + help_text
        + "\n"
        + CODE_BLOCK_END
        + "\n"
        + markdown_text[end_pos:]
    )


def update_file(file_path: Path, help_text: str, check: bool) -> bool:
    """Update one markdown file and return whether it changed."""
    markdown_text = file_path.read_text(encoding="utf-8")
    updated_text = inject_help(markdown_text, help_text)
    if updated_text == markdown_text:
        return False
    if check:
        return True
    file_path.write_text(updated_text, encoding="utf-8")
    print(f"Updated {file_path}")
    return True


def main() -> int:
    """Update or validate CLI help snapshots in markdown docs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check whether the tracked help snapshots are up to date.",
    )
    args = parser.parse_args()

    help_text = get_help_text()
    changed_files: list[Path] = []
    for file_path in TARGET_MARKDOWN_FILES:
        if update_file(file_path, help_text, check=args.check):
            changed_files.append(file_path)

    if args.check and changed_files:
        for file_path in changed_files:
            print(f"Out of date: {file_path}", file=sys.stderr)
        print(
            "\nRun 'python scripts/update_command_help_on_markdown.py' to regenerate.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
