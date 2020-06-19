from pathlib import Path

import pytest

from fastapi_code_generator.__main__ import generate_code


@pytest.mark.parametrize("oas_file", Path("tests/").glob("*.yaml"))
def test_generate_simple(oas_file):
    ret = generate_code(
        input_name=oas_file.name,
        input_text=oas_file.read_text(),
        output_dir="tmp" / oas_file.with_suffix(".app"),
        template_dir=None,
    )
