"""Build prompt data from cli_doc collection.

Generates fastapi_code_generator/prompt_data.py containing
option descriptions extracted from cli_doc markers.

Usage:
    pytest --collect-cli-docs -p no:xdist
    python scripts/build_prompt_data.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
COLLECTION_PATH = PROJECT_ROOT / "tests" / "cli_doc" / ".cli_doc_collection.json"
OUTPUT_PATH = PROJECT_ROOT / "fastapi_code_generator" / "prompt_data.py"


def build_prompt_data(*, check: bool = False) -> int:
    if not COLLECTION_PATH.exists():
        print(f"Collection file not found: {COLLECTION_PATH}", file=sys.stderr)
        print("Run: pytest --collect-cli-docs -p no:xdist", file=sys.stderr)
        return 1

    with COLLECTION_PATH.open(encoding="utf-8") as f:
        collection = json.load(f)

    descriptions: dict[str, str] = {}
    for item in collection.get("items", []):
        option_description = item.get("option_description", "")
        if not option_description:
            continue
        first_line = option_description.split("\n")[0].strip()
        for option in item.get("marker_kwargs", {}).get("options", []):
            if option not in descriptions:
                descriptions[option] = first_line

    lines = [
        '"""Auto-generated prompt data from cli_doc collection.',
        "",
        "DO NOT EDIT MANUALLY. Run: python scripts/build_prompt_data.py",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "# Option descriptions extracted from cli_doc markers",
        "OPTION_DESCRIPTIONS: dict[str, str] = {",
    ]
    for option, description in sorted(descriptions.items()):
        escaped_description = description.replace("\\", "\\\\").replace('"', '\\"')
        max_description_length = 120 - len(f'    "{option}": "",')
        if len(escaped_description) > max_description_length:
            truncated_description = escaped_description[: max_description_length - 3]
            truncated_description = truncated_description.removesuffix("\\")
            escaped_description = truncated_description + "..."
        lines.append(f'    "{option}": "{escaped_description}",')
    lines.extend(("}", ""))

    content = "\n".join(lines)

    if check:
        if not OUTPUT_PATH.exists():
            print(f"Output file not found: {OUTPUT_PATH}", file=sys.stderr)
            return 1
        existing = OUTPUT_PATH.read_text(encoding="utf-8")
        if existing != content:
            print(f"Content mismatch: {OUTPUT_PATH}", file=sys.stderr)
            return 1
        print(f"OK: {OUTPUT_PATH}")
        return 0

    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"Generated: {OUTPUT_PATH} ({len(descriptions)} options)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build prompt data from cli_doc collection")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if prompt data is up to date without modifying files",
    )
    args = parser.parse_args()
    return build_prompt_data(check=args.check)


if __name__ == "__main__":
    sys.exit(main())
