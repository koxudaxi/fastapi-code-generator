from __future__ import annotations

from typing import Any

import pytest

from tests.cli_doc.test_cli_doc_coverage import (
    MANUAL_DOCS,
    get_all_canonical_options,
    get_canonical_option,
)


@pytest.fixture(scope="module")
def collected_options(request: pytest.FixtureRequest) -> set[str]:
    items: list[dict[str, Any]] = getattr(request.config, "_cli_doc_items", [])
    options: set[str] = set()
    for item in items:
        options.update(item.get("marker_kwargs", {}).get("options", []))
    return {get_canonical_option([option]) for option in options}


def test_manual_doc_options_exist_in_cli() -> None:
    orphan = MANUAL_DOCS - get_all_canonical_options()
    assert not orphan, "Options in MANUAL_DOCS but not in CLI:\n" + "\n".join(
        f"  - {option}" for option in sorted(orphan)
    )


def test_cli_doc_marker_options_exist_in_cli(collected_options: set[str]) -> None:
    missing = collected_options - get_all_canonical_options()
    assert not missing, "Options in cli_doc markers but not in CLI:\n" + "\n".join(
        f"  - {option}" for option in sorted(missing)
    )
