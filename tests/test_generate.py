from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from freezegun import freeze_time

from fastapi_code_generator.__main__ import generate_code

OPEN_API_DIR_NAME = 'openapi'

DATA_DIR = Path(__file__).parent / 'data'

OPEN_API_DIR = DATA_DIR / OPEN_API_DIR_NAME

EXPECTED_DIR = DATA_DIR / 'expected'


@pytest.mark.parametrize("oas_file", OPEN_API_DIR.glob("*.yaml"))
@freeze_time("2020-06-19")
def test_generate_simple(oas_file):
    with TemporaryDirectory() as tmp_dir:
        output_dir = Path(tmp_dir) / oas_file.stem
        generate_code(
            input_name=oas_file.name,
            input_text=oas_file.read_text(),
            output_dir=output_dir,
            template_dir=None,
        )
        expected_dir = EXPECTED_DIR / OPEN_API_DIR_NAME / oas_file.stem
        output_files = sorted(list(output_dir.glob('*')))
        expected_files = sorted(list(expected_dir.glob('*')))
        assert [f.name for f in output_files] == [f.name for f in expected_files]
        for output_file, expected_file in zip(output_files, expected_files):
            assert output_file.read_text() == expected_file.read_text()