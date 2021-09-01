from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import call

import pytest
from freezegun import freeze_time

from fastapi_code_generator.__main__ import generate_code

OPEN_API_DEFAULT_TEMPLATE_DIR_NAME = Path('openapi') / 'default_template'
OPEN_API_SECURITY_TEMPLATE_DIR_NAME = Path('openapi') / 'custom_template_security'
OPEN_API_REMOTE_REF_DIR_NAME = Path('openapi') / 'remote_ref'

DATA_DIR = Path(__file__).parent / 'data'

EXPECTED_DIR = DATA_DIR / 'expected'


@pytest.mark.parametrize(
    "oas_file", (DATA_DIR / OPEN_API_DEFAULT_TEMPLATE_DIR_NAME).glob("*.yaml")
)
@freeze_time("2020-06-19")
def test_generate_default_template(oas_file):
    with TemporaryDirectory() as tmp_dir:
        output_dir = Path(tmp_dir) / oas_file.stem
        generate_code(
            input_name=oas_file.name,
            input_text=oas_file.read_text(),
            output_dir=output_dir,
            template_dir=None,
        )
        expected_dir = EXPECTED_DIR / OPEN_API_DEFAULT_TEMPLATE_DIR_NAME / oas_file.stem
        output_files = sorted(list(output_dir.glob('*')))
        expected_files = sorted(list(expected_dir.glob('*')))
        assert [f.name for f in output_files] == [f.name for f in expected_files]
        for output_file, expected_file in zip(output_files, expected_files):
            assert output_file.read_text() == expected_file.read_text()


@pytest.mark.parametrize(
    "oas_file", (DATA_DIR / OPEN_API_SECURITY_TEMPLATE_DIR_NAME).glob("*.yaml")
)
@freeze_time("2020-06-19")
def test_generate_custom_security_template(oas_file):
    with TemporaryDirectory() as tmp_dir:
        output_dir = Path(tmp_dir) / oas_file.stem
        generate_code(
            input_name=oas_file.name,
            input_text=oas_file.read_text(),
            output_dir=output_dir,
            template_dir=DATA_DIR / 'custom_template' / 'security',
        )
        expected_dir = (
            EXPECTED_DIR / OPEN_API_SECURITY_TEMPLATE_DIR_NAME / oas_file.stem
        )
        output_files = sorted(list(output_dir.glob('*')))
        expected_files = sorted(list(expected_dir.glob('*')))
        assert [f.name for f in output_files] == [f.name for f in expected_files]
        for output_file, expected_file in zip(output_files, expected_files):
            assert output_file.read_text() == expected_file.read_text()


@freeze_time("2020-06-19")
def test_generate_remote_ref(mocker):
    oas_file = DATA_DIR / OPEN_API_REMOTE_REF_DIR_NAME / 'body_and_parameters.yaml'
    person_response = mocker.Mock()
    person_response.text = oas_file.read_text()
    httpx_get_mock = mocker.patch('httpx.get', side_effect=[person_response])

    with TemporaryDirectory() as tmp_dir:
        output_dir = Path(tmp_dir) / oas_file.stem
        generate_code(
            input_name=oas_file.name,
            input_text=oas_file.read_text(),
            output_dir=output_dir,
            template_dir=None,
        )
        httpx_get_mock.assert_has_calls(
            [call('https://schema.example', headers=None), ]
        )
        expected_dir = EXPECTED_DIR / OPEN_API_REMOTE_REF_DIR_NAME / oas_file.stem
        output_files = sorted(list(output_dir.glob('*')))
        expected_files = sorted(list(expected_dir.glob('*')))
        assert [f.name for f in output_files] == [f.name for f in expected_files]
        for output_file, expected_file in zip(output_files, expected_files):
            assert output_file.read_text() == expected_file.read_text()
