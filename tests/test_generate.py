from fastapi_code_generator.__main__ import generate_code
from pathlib import Path
import pytest


@pytest.mark.parametrize("oas_file", Path("tests/").glob("*.yaml"))
def test_generate_simple(oas_file):
    input_file = oas_file  # "tests" / Path('simple.yaml')
    ret = generate_code(input_name=input_file.name, input_text=input_file.read_text(), output_dir="tmp" / oas_file.with_suffix(".app"),
                        template_dir=None)
