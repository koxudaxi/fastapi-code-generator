from __future__ import annotations

from typing import Any

import pytest
from typer.main import get_command

from fastapi_code_generator.__main__ import app

MANUAL_DOCS = {"--install-completion", "--show-completion"}
EXTRA_OPTIONS = {"--help", "--version"}


def get_canonical_option(option_strings: list[str]) -> str:
    return sorted(option_strings, key=lambda option: (len(option), option))[-1]


def get_all_canonical_options() -> set[str]:
    options = set(EXTRA_OPTIONS)
    command = get_command(app)
    for param in command.params:
        option_strings = [
            *getattr(param, "opts", []),
            *getattr(param, "secondary_opts", []),
        ]
        if not option_strings:  # pragma: no cover
            continue
        options.add(get_canonical_option(option_strings))
    return options


@pytest.fixture(scope="module")
def collected_options(request: pytest.FixtureRequest) -> set[str]:
    items: list[dict[str, Any]] = getattr(request.config, "_cli_doc_items", [])
    options: set[str] = set()
    for item in items:
        options.update(item.get("marker_kwargs", {}).get("options", []))
    return {get_canonical_option([option]) for option in options}


def test_all_options_have_cli_doc_markers(collected_options: set[str]) -> None:
    missing = (get_all_canonical_options() - MANUAL_DOCS) - collected_options
    assert not missing, "CLI options missing cli_doc marker:\n" + "\n".join(
        f"  - {option}" for option in sorted(missing)
    )
