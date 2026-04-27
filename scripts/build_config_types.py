"""Generate TypedDict helpers from GenerateConfig."""

from __future__ import annotations

import argparse

from fastapi_code_generator.config import update_generated_types


def main() -> int:
    """Run the builder."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return update_generated_types(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
