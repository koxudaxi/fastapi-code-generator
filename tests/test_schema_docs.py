from __future__ import annotations

from scripts.build_schema_docs import (
    DOCS_PATH,
    FIXTURE_SUITES,
    _suite_fixture_paths,
    render_document,
)


def test_fixture_suites_are_backed_by_files() -> None:
    for suite in FIXTURE_SUITES:
        assert _suite_fixture_paths(suite.directory), suite.directory


def test_supported_formats_doc_is_up_to_date() -> None:
    assert DOCS_PATH.read_text(encoding="utf-8") == render_document()
