"""Update GitHub Action version references in documentation."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"
README_FILE = ROOT_DIR / "README.md"
PATTERN = re.compile(r"(koxudaxi/fastapi-code-generator@)(\d+\.\d+\.\d+)")


def get_latest_release_version() -> str:
    """Get the latest release tag from GitHub."""
    result = subprocess.run(
        ["gh", "release", "list", "--limit", "1", "--exclude-drafts", "--json", "tagName", "-q", ".[0].tagName"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def update_file(file_path: Path, version: str, *, check: bool) -> bool:
    """Update action version references in one file."""
    content = file_path.read_text(encoding="utf-8")
    new_content = PATTERN.sub(rf"\g<1>{version}", content)
    if content == new_content:
        return False
    if check:
        return True
    file_path.write_text(new_content, encoding="utf-8")
    return True


def main() -> int:
    """Run the updater."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    try:
        version = get_latest_release_version()
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"Error getting latest release: {exc}", file=sys.stderr)
        return 1

    target_files = list(DOCS_DIR.rglob("*.md"))
    if README_FILE.exists():
        target_files.append(README_FILE)
    updated_files = [path for path in target_files if update_file(path, version, check=args.check)]
    if args.check and updated_files:
        for path in updated_files:
            print(f"Out of date: {path.relative_to(ROOT_DIR)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
