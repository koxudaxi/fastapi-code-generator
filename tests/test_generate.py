import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import call

import pytest
from freezegun import freeze_time

from fastapi_code_generator.__main__ import generate_code

OPEN_API_DEFAULT_TEMPLATE_DIR_NAME = Path('openapi') / 'default_template'
OPEN_API_SECURITY_TEMPLATE_DIR_NAME = Path('openapi') / 'custom_template_security'
OPEN_API_REMOTE_REF_DIR_NAME = Path('openapi') / 'remote_ref'
OPEN_API_DISABLE_TIMESTAMP_DIR_NAME = Path('openapi') / 'disable_timestamp'
OPEN_API_USING_ROUTERS_DIR_NAME = Path('openapi') / 'using_routers'

DATA_DIR = Path(__file__).parent / 'data'

EXPECTED_DIR = DATA_DIR / 'expected'

BUILTIN_MODULAR_TEMPLATE_DIR = DATA_DIR / 'modular_template'

SPECIFIC_TAGS = 'Wild Boars, Fat Cats'

ENCODING = 'utf-8'


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
            encoding=ENCODING,
            output_dir=output_dir,
            template_dir=None,
        )
        expected_dir = EXPECTED_DIR / OPEN_API_DEFAULT_TEMPLATE_DIR_NAME / oas_file.stem
        output_files = sorted(list(output_dir.glob('*')))
        expected_files = sorted(list(expected_dir.glob('*')))
        assert [f.name for f in output_files] == [f.name for f in expected_files]
        for output_file, expected_file in zip(output_files, expected_files):
            assert output_file.read_text() == expected_file.read_text(), oas_file


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
            encoding=ENCODING,
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
            encoding=ENCODING,
            output_dir=output_dir,
            template_dir=None,
        )
        httpx_get_mock.assert_has_calls(
            [
                call(
                    'https://schema.example',
                    headers=None,
                    verify=True,
                    follow_redirects=True,
                    params=None,
                ),
            ]
        )
        expected_dir = EXPECTED_DIR / OPEN_API_REMOTE_REF_DIR_NAME / oas_file.stem
        output_files = sorted(list(output_dir.glob('*')))
        expected_files = sorted(list(expected_dir.glob('*')))
        assert [f.name for f in output_files] == [f.name for f in expected_files]
        for output_file, expected_file in zip(output_files, expected_files):
            assert output_file.read_text() == expected_file.read_text()


@pytest.mark.parametrize(
    "oas_file", (DATA_DIR / OPEN_API_DISABLE_TIMESTAMP_DIR_NAME).glob("*.yaml")
)
@freeze_time("2020-06-19")
def test_disable_timestamp(oas_file):
    with TemporaryDirectory() as tmp_dir:
        output_dir = Path(tmp_dir) / oas_file.stem
        generate_code(
            input_name=oas_file.name,
            input_text=oas_file.read_text(),
            encoding=ENCODING,
            output_dir=output_dir,
            template_dir=None,
            disable_timestamp=True,
        )
        expected_dir = (
            EXPECTED_DIR / OPEN_API_DISABLE_TIMESTAMP_DIR_NAME / oas_file.stem
        )
        output_files = sorted(list(output_dir.glob('*')))
        expected_files = sorted(list(expected_dir.glob('*')))
        assert [f.name for f in output_files] == [f.name for f in expected_files]
        for output_file, expected_file in zip(output_files, expected_files):
            assert output_file.read_text() == expected_file.read_text(), oas_file


@pytest.mark.parametrize(
    "oas_file", (DATA_DIR / OPEN_API_USING_ROUTERS_DIR_NAME).glob("*.yaml")
)
@freeze_time("2023-04-11")
def test_generate_using_routers(oas_file):
    with TemporaryDirectory() as tmp_dir:
        output_dir = Path(tmp_dir) / oas_file.stem
        Path(output_dir / "routers").mkdir(parents=True, exist_ok=True)
        generate_code(
            input_name=oas_file.name,
            input_text=oas_file.read_text(),
            encoding=ENCODING,
            output_dir=output_dir,
            template_dir=BUILTIN_MODULAR_TEMPLATE_DIR,
            generate_routers=True,
        )
        expected_dir = EXPECTED_DIR / OPEN_API_USING_ROUTERS_DIR_NAME / oas_file.stem
        output_files = sorted(list(output_dir.glob('*')))
        expected_files = sorted(list(expected_dir.glob('*')))
        assert [f.name for f in output_files] == [f.name for f in expected_files]
        for output_file, expected_file in zip(output_files, expected_files):
            if output_file.is_dir() and expected_file.is_dir():
                output_inners = sorted(list((output_dir / output_file).glob('*')))
                expected_inners = sorted(list((expected_dir / expected_file).glob('*')))
                for output_inner, expected_inner in zip(output_inners, expected_inners):
                    assert output_inner.read_text() == expected_inner.read_text()
            else:
                assert output_file.read_text() == expected_file.read_text(), oas_file


@pytest.mark.parametrize(
    "oas_file", (DATA_DIR / OPEN_API_USING_ROUTERS_DIR_NAME).glob("*.yaml")
)
@freeze_time("2023-04-11")
def test_generate_modify_specific_routers(oas_file):
    with TemporaryDirectory() as tmp_dir:
        output_dir = Path(tmp_dir) / (oas_file.stem + '_modify_specific_routers')
        # modified contains generated source files. Some of them will be regenerated in this test.
        modified_dir = (
            EXPECTED_DIR
            / 'openapi/modify_specific_routers/modified/using_routers_example'
        )
        shutil.copytree(modified_dir, output_dir)

        Path(output_dir / "routers").mkdir(parents=True, exist_ok=True)
        generate_code(
            input_name=oas_file.name,
            input_text=oas_file.read_text(),
            encoding=ENCODING,
            output_dir=output_dir,
            template_dir=BUILTIN_MODULAR_TEMPLATE_DIR,
            generate_routers=True,
            specify_tags=SPECIFIC_TAGS,
        )
        expected_dir = (
            EXPECTED_DIR / 'openapi/modify_specific_routers/expected' / oas_file.stem
        )
        output_files = sorted(list(output_dir.glob('*')))
        expected_files = sorted(list(expected_dir.glob('*')))
        assert [f.name for f in output_files] == [f.name for f in expected_files]
        for output_file, expected_file in zip(output_files, expected_files):
            if output_file.is_dir() and expected_file.is_dir():
                output_inners = sorted(list((output_dir / output_file).glob('*')))
                expected_inners = sorted(list((expected_dir / expected_file).glob('*')))
                for output_inner, expected_inner in zip(output_inners, expected_inners):
                    assert output_inner.read_text() == expected_inner.read_text()
            else:
                assert output_file.read_text() == expected_file.read_text()
