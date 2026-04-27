from __future__ import annotations

import json
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import as_file, files
from pathlib import Path
from shutil import copy2, copytree
from threading import Thread
from typing import Iterator

import pytest
import yaml

from fastapi_code_generator.cli import generate_code
from tests.conftest import freeze_time, validate_generated_code
from tests.main.conftest import (
    DATA_PATH,
    EXPECTED_OPENAPI_PATH,
    run_cli_and_assert,
    run_main_with_args,
)

OPEN_API_DEFAULT_TEMPLATE_DIR_NAME = Path("openapi") / "default_template"
OPEN_API_SECURITY_TEMPLATE_DIR_NAME = Path("openapi") / "custom_template_security"
OPEN_API_REMOTE_REF_DIR_NAME = Path("openapi") / "remote_ref"
OPEN_API_DISABLE_TIMESTAMP_DIR_NAME = Path("openapi") / "disable_timestamp"
OPEN_API_USING_ROUTERS_DIR_NAME = Path("openapi") / "using_routers"
OPEN_API_COVERAGE_DIR_NAME = Path("openapi") / "coverage"
MODIFY_SPECIFIC_ROUTERS_EXPECTED_DIR_NAME = Path("modify_specific_routers")

BUILTIN_MODULAR_TEMPLATE_DIR = DATA_PATH / "modular_template"
SPECIFIC_TAGS = "Wild Boars, Fat Cats"


@pytest.mark.cli_doc(
    options=["--help"],
    option_description="Show the CLI help message.",
    cli_args=["--help"],
    expected_stdout="cli/help.txt",
)
def test_show_help(capsys: pytest.CaptureFixture[str]) -> None:
    assert run_main_with_args(["--help"]) == 0
    assert "Usage: fastapi-codegen" in capsys.readouterr().out


@pytest.mark.cli_doc(
    options=["--version"],
    option_description="Show the installed fastapi-codegen version.",
    cli_args=["--version"],
    expected_stdout="cli/version.txt",
)
def test_show_version(capsys: pytest.CaptureFixture[str]) -> None:
    assert run_main_with_args(["--version"]) == 0
    assert capsys.readouterr().out.startswith("fastapi-codegen ")


def test_show_version_with_other_options(capsys: pytest.CaptureFixture[str]) -> None:
    assert (
        run_main_with_args(
            [
                "--version",
                "--input",
                str(DATA_PATH / OPEN_API_DEFAULT_TEMPLATE_DIR_NAME / "simple.yaml"),
                "--output",
                "app",
            ]
        )
        == 0
    )
    assert capsys.readouterr().out.startswith("fastapi-codegen ")


def test_missing_required_options(capsys: pytest.CaptureFixture[str]) -> None:
    assert run_main_with_args([]) == 2
    assert "Missing option '--input'" in capsys.readouterr().err


@freeze_time("2020-06-19T00:00:00.123456Z")
def test_generate_into_existing_output_dir(output_dir: Path) -> None:
    output_dir.mkdir(parents=True)
    run_cli_and_assert(
        input_path=DATA_PATH / OPEN_API_DEFAULT_TEMPLATE_DIR_NAME / "simple.yaml",
        output_path=output_dir,
        expected_path=EXPECTED_OPENAPI_PATH / "default_template" / "simple",
    )


@pytest.mark.cli_doc(
    options=["--output"],
    option_description="Directory where the generated FastAPI application is written.",
    cli_args=["--input", "openapi/default_template/simple.yaml", "--output", "app"],
    input_schema="openapi/default_template/simple.yaml",
    golden_output="openapi/default_template/simple/main.py",
    related_options=["--input"],
)
@pytest.mark.cli_doc(
    options=["--input"],
    option_description="Generate a FastAPI application from an OpenAPI input file.",
    cli_args=["--input", "openapi/default_template/simple.yaml", "--output", "app"],
    input_schema="openapi/default_template/simple.yaml",
    golden_output="openapi/default_template/simple/main.py",
    related_options=["--output"],
)
@pytest.mark.parametrize(
    "oas_file",
    sorted((DATA_PATH / OPEN_API_DEFAULT_TEMPLATE_DIR_NAME).glob("*.yaml")),
    ids=lambda path: path.stem,
)
@freeze_time("2020-06-19")
def test_generate_default_template(oas_file: Path, output_dir: Path) -> None:
    run_cli_and_assert(
        input_path=oas_file,
        output_path=output_dir,
        expected_path=EXPECTED_OPENAPI_PATH / "default_template" / oas_file.stem,
    )


@pytest.mark.cli_doc(
    options=["--template-dir"],
    option_description="Render generated files with a custom template directory.",
    cli_args=[
        "--input",
        "openapi/custom_template_security/custom_security.yaml",
        "--output",
        "app",
        "--template-dir",
        "custom_template/security",
    ],
    input_schema="openapi/custom_template_security/custom_security.yaml",
    golden_output="openapi/custom_template_security/custom_security/main.py",
)
@pytest.mark.parametrize(
    "oas_file",
    sorted((DATA_PATH / OPEN_API_SECURITY_TEMPLATE_DIR_NAME).glob("*.yaml")),
    ids=lambda path: path.stem,
)
@freeze_time("2020-06-19")
def test_generate_custom_security_template(oas_file: Path, output_dir: Path) -> None:
    run_cli_and_assert(
        input_path=oas_file,
        output_path=output_dir,
        expected_path=EXPECTED_OPENAPI_PATH
        / "custom_template_security"
        / oas_file.stem,
        extra_args=["--template-dir", str(DATA_PATH / "custom_template" / "security")],
    )


class SchemaRequestHandler(BaseHTTPRequestHandler):
    schema_text = ""

    def do_GET(self) -> None:  # noqa: N802
        self.send_response(200)
        self.send_header("Content-Type", "application/yaml")
        self.end_headers()
        self.wfile.write(self.schema_text.encode("utf-8"))

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        del format, args


@contextmanager
def serve_schema(schema_text: str) -> Iterator[str]:
    handler = type(
        "RemoteSchemaHandler", (SchemaRequestHandler,), {"schema_text": schema_text}
    )
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/schema.yaml"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


@freeze_time("2020-06-19")
def test_generate_remote_ref(tmp_path: Path, output_dir: Path) -> None:
    oas_file = DATA_PATH / OPEN_API_REMOTE_REF_DIR_NAME / "body_and_parameters.yaml"
    remote_schema = oas_file.read_text(encoding="utf-8")
    with serve_schema(remote_schema) as schema_url:
        input_path = tmp_path / oas_file.name
        input_path.write_text(
            oas_file.read_text(encoding="utf-8").replace(
                "https://schema.example", schema_url
            ),
            encoding="utf-8",
        )
        run_cli_and_assert(
            input_path=input_path,
            output_path=output_dir,
            expected_path=EXPECTED_OPENAPI_PATH / "remote_ref" / oas_file.stem,
        )


@freeze_time("2020-06-19")
def test_generate_from_json_input(tmp_path: Path, output_dir: Path) -> None:
    source = DATA_PATH / OPEN_API_DEFAULT_TEMPLATE_DIR_NAME / "simple.yaml"
    json_input = tmp_path / "simple.json"
    json_input.write_text(
        json.dumps(yaml.safe_load(source.read_text(encoding="utf-8"))),
        encoding="utf-8",
    )
    assert (
        run_main_with_args(
            [
                "--input",
                str(json_input),
                "--output",
                str(output_dir),
            ]
        )
        == 0
    )
    expected_dir = EXPECTED_OPENAPI_PATH / "default_template" / "simple"
    assert sorted(
        path.relative_to(output_dir) for path in output_dir.rglob("*") if path.is_file()
    ) == [Path("main.py"), Path("models.py")]
    for relative_path in [Path("main.py"), Path("models.py")]:
        generated = output_dir.joinpath(relative_path).read_text(encoding="utf-8")
        expected = expected_dir.joinpath(relative_path).read_text(encoding="utf-8")
        assert generated.replace("simple.json", "simple.yaml").replace(
            "\r\n", "\n"
        ) == expected.replace("\r\n", "\n")
    validate_generated_code(output_dir)


@freeze_time("2020-06-19")
def test_generate_escapes_aliases_in_parameter_defaults(output_dir: Path) -> None:
    spec = """openapi: 3.0.0
info:
  title: Escaped aliases
  version: 1.0.0
paths:
  /pets:
    get:
      responses:
        '200':
          description: ok
      parameters:
        - name: message-"\\\\texts
          in: query
          required: false
          schema:
            type: array
            items:
              type: string
        - name: X-"\\\\Token
          in: header
          required: false
          schema:
            type: string
"""
    generate_code("escaped_aliases.yaml", spec, "utf-8", output_dir, None)

    generated = (output_dir / "main.py").read_text(encoding="utf-8")

    assert "Query(None, alias='message-\"\\\\\\\\texts')" in generated
    assert "Header(None, alias='X-\"\\\\\\\\Token')" in generated
    validate_generated_code(output_dir)


@pytest.mark.cli_doc(
    options=["--encoding"],
    option_description="Read the input schema using an explicit text encoding.",
    cli_args=[
        "--input",
        "openapi/default_template/simple.yaml",
        "--output",
        "app",
        "--encoding",
        "utf-16",
    ],
    input_schema="openapi/default_template/simple.yaml",
    golden_output="openapi/default_template/simple/main.py",
)
@freeze_time("2020-06-19")
def test_generate_with_encoding(tmp_path: Path, output_dir: Path) -> None:
    source = DATA_PATH / OPEN_API_DEFAULT_TEMPLATE_DIR_NAME / "simple.yaml"
    encoded_input = tmp_path / "simple-utf16.yaml"
    encoded_input.write_text(source.read_text(encoding="utf-8"), encoding="utf-16")
    assert (
        run_main_with_args(
            [
                "--input",
                str(encoded_input),
                "--output",
                str(output_dir),
                "--encoding",
                "utf-16",
            ]
        )
        == 0
    )
    expected_dir = EXPECTED_OPENAPI_PATH / "default_template" / "simple"
    assert sorted(
        path.relative_to(output_dir) for path in output_dir.rglob("*") if path.is_file()
    ) == [Path("main.py"), Path("models.py")]
    for relative_path in [Path("main.py"), Path("models.py")]:
        generated_bytes = output_dir.joinpath(relative_path).read_bytes()
        generated = (
            generated_bytes.decode("utf-16")
            if generated_bytes.startswith((b"\xff\xfe", b"\xfe\xff"))
            else generated_bytes.decode("utf-8")
        )
        expected = expected_dir.joinpath(relative_path).read_text(encoding="utf-8")
        assert generated.replace("simple-utf16.yaml", "simple.yaml").replace(
            "\r\n", "\n"
        ) == expected.replace("\r\n", "\n")
        compile(generated, str(output_dir.joinpath(relative_path)), "exec")


@pytest.mark.cli_doc(
    options=["--disable-timestamp"],
    option_description="Omit the generated timestamp header from output files.",
    cli_args=[
        "--input",
        "openapi/disable_timestamp/simple.yaml",
        "--output",
        "app",
        "--disable-timestamp",
    ],
    input_schema="openapi/disable_timestamp/simple.yaml",
    golden_output="openapi/disable_timestamp/simple/main.py",
)
@pytest.mark.parametrize(
    "oas_file",
    sorted((DATA_PATH / OPEN_API_DISABLE_TIMESTAMP_DIR_NAME).glob("*.yaml")),
    ids=lambda path: path.stem,
)
@freeze_time("2020-06-19")
def test_disable_timestamp(oas_file: Path, output_dir: Path) -> None:
    run_cli_and_assert(
        input_path=oas_file,
        output_path=output_dir,
        expected_path=EXPECTED_OPENAPI_PATH / "disable_timestamp" / oas_file.stem,
        extra_args=["--disable-timestamp"],
    )


@pytest.mark.cli_doc(
    options=["--generate-routers"],
    option_description="Generate modular router files from tagged OpenAPI operations.",
    cli_args=[
        "--input",
        "openapi/using_routers/using_routers_example.yaml",
        "--output",
        "app",
        "--template-dir",
        "modular_template",
        "--generate-routers",
    ],
    input_schema="openapi/using_routers/using_routers_example.yaml",
    golden_output="openapi/using_routers/using_routers_example/main.py",
)
@pytest.mark.parametrize(
    "oas_file",
    sorted((DATA_PATH / OPEN_API_USING_ROUTERS_DIR_NAME).glob("*.yaml")),
    ids=lambda path: path.stem,
)
@freeze_time("2023-04-11")
def test_generate_using_routers(oas_file: Path, output_dir: Path) -> None:
    run_cli_and_assert(
        input_path=oas_file,
        output_path=output_dir,
        expected_path=EXPECTED_OPENAPI_PATH / "using_routers" / oas_file.stem,
        extra_args=[
            "--template-dir",
            str(BUILTIN_MODULAR_TEMPLATE_DIR),
            "--generate-routers",
        ],
    )


def test_generate_router_name_from_hyphenated_tag(output_dir: Path) -> None:
    spec = json.dumps(
        {
            "openapi": "3.0.0",
            "info": {"title": "Example", "version": "1.0.0"},
            "paths": {
                "/items": {
                    "get": {
                        "tags": ["Foo-Bar"],
                        "responses": {"200": {"description": "OK"}},
                    }
                }
            },
        }
    )

    generate_code(
        "hyphenated_tag.yaml",
        spec,
        "utf-8",
        output_dir,
        BUILTIN_MODULAR_TEMPLATE_DIR,
        disable_timestamp=True,
        generate_routers=True,
    )

    assert output_dir.joinpath("routers", "foo_bar.py").exists()
    assert "from .routers import foo_bar" in output_dir.joinpath("main.py").read_text(
        encoding="utf-8"
    )
    validate_generated_code(output_dir)


@pytest.mark.cli_doc(
    options=["--specify-tags"],
    option_description="Regenerate only the routers matching a comma-separated tag list.",
    cli_args=[
        "--input",
        "openapi/using_routers/using_routers_example.yaml",
        "--output",
        "app",
        "--template-dir",
        "modular_template",
        "--generate-routers",
        "--specify-tags",
        "Wild Boars, Fat Cats",
    ],
    input_schema="openapi/using_routers/using_routers_example.yaml",
    golden_output="openapi/modify_specific_routers/expected/using_routers_example/main.py",
)
@pytest.mark.parametrize(
    "oas_file",
    sorted((DATA_PATH / OPEN_API_USING_ROUTERS_DIR_NAME).glob("*.yaml")),
    ids=lambda path: path.stem,
)
@freeze_time("2023-04-11")
def test_generate_modify_specific_routers(oas_file: Path, output_dir: Path) -> None:
    modified_dir = (
        EXPECTED_OPENAPI_PATH
        / MODIFY_SPECIFIC_ROUTERS_EXPECTED_DIR_NAME
        / "modified"
        / oas_file.stem
    )
    copytree(modified_dir, output_dir)
    run_cli_and_assert(
        input_path=oas_file,
        output_path=output_dir,
        expected_path=EXPECTED_OPENAPI_PATH
        / MODIFY_SPECIFIC_ROUTERS_EXPECTED_DIR_NAME
        / "expected"
        / oas_file.stem,
        extra_args=[
            "--template-dir",
            str(BUILTIN_MODULAR_TEMPLATE_DIR),
            "--generate-routers",
            "--specify-tags",
            SPECIFIC_TAGS,
        ],
    )


@freeze_time("2023-04-11")
def test_generate_specific_tags_without_existing_main(output_dir: Path) -> None:
    run_cli_and_assert(
        input_path=DATA_PATH
        / OPEN_API_USING_ROUTERS_DIR_NAME
        / "using_routers_example.yaml",
        output_path=output_dir,
        expected_path=EXPECTED_OPENAPI_PATH / "using_routers" / "using_routers_example",
        extra_args=[
            "--template-dir",
            str(BUILTIN_MODULAR_TEMPLATE_DIR),
            "--generate-routers",
            "--specify-tags",
            SPECIFIC_TAGS,
        ],
    )


@freeze_time("2023-04-11")
def test_generate_specific_tags_with_existing_main_without_router_includes(
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True)
    output_dir.joinpath("main.py").write_text(
        "from fastapi import FastAPI\n\napp = FastAPI()\n",
        encoding="utf-8",
    )
    run_cli_and_assert(
        input_path=DATA_PATH
        / OPEN_API_USING_ROUTERS_DIR_NAME
        / "using_routers_example.yaml",
        output_path=output_dir,
        expected_path=EXPECTED_OPENAPI_PATH / "using_routers" / "using_routers_example",
        extra_args=[
            "--template-dir",
            str(BUILTIN_MODULAR_TEMPLATE_DIR),
            "--generate-routers",
            "--specify-tags",
            SPECIFIC_TAGS,
        ],
    )


@freeze_time("2020-06-19")
def test_generate_non_200_responses(output_dir: Path) -> None:
    run_cli_and_assert(
        input_path=DATA_PATH / OPEN_API_COVERAGE_DIR_NAME / "non_200_responses.yaml",
        output_path=output_dir,
        expected_path=EXPECTED_OPENAPI_PATH / "coverage" / "non_200_responses",
    )


@pytest.mark.cli_doc(
    options=["--enum-field-as-literal"],
    option_description="Render enum fields as Literal annotations.",
    cli_args=[
        "--input",
        "openapi/default_template/duplicate_anonymus_parameter.yaml",
        "--output",
        "app",
        "--enum-field-as-literal",
        "all",
    ],
    input_schema="openapi/default_template/duplicate_anonymus_parameter.yaml",
    golden_output="openapi/coverage/enum_field_as_literal/models.py",
)
@freeze_time("2020-06-19")
def test_generate_with_enum_field_as_literal(output_dir: Path) -> None:
    run_cli_and_assert(
        input_path=DATA_PATH
        / OPEN_API_DEFAULT_TEMPLATE_DIR_NAME
        / "duplicate_anonymus_parameter.yaml",
        output_path=output_dir,
        expected_path=EXPECTED_OPENAPI_PATH / "coverage" / "enum_field_as_literal",
        extra_args=["--enum-field-as-literal", "all"],
    )


@pytest.mark.cli_doc(
    options=["--use-annotated"],
    option_description="Render model field constraints with typing.Annotated.",
    cli_args=[
        "--input",
        "openapi/default_template/recursion.yaml",
        "--output",
        "app",
        "--use-annotated",
    ],
    input_schema="openapi/default_template/recursion.yaml",
    golden_output="openapi/default_template/recursion/models.py",
)
@freeze_time("2020-06-19")
def test_generate_with_use_annotated(output_dir: Path) -> None:
    assert (
        run_main_with_args(
            [
                "--input",
                str(DATA_PATH / OPEN_API_DEFAULT_TEMPLATE_DIR_NAME / "recursion.yaml"),
                "--output",
                str(output_dir),
                "--use-annotated",
            ]
        )
        == 0
    )

    models = output_dir.joinpath("models.py").read_text(encoding="utf-8")
    assert "from typing import Annotated, Optional" in models
    assert (
        "Field(examples=['5abbe4b7ddc1b351ef961414'], " "pattern='^[0-9a-fA-F]{24}$')"
    ) in models
    validate_generated_code(output_dir)


@pytest.mark.parametrize(
    "oas_file",
    sorted((DATA_PATH / OPEN_API_COVERAGE_DIR_NAME).glob("callbacks*.yaml")),
    ids=lambda path: path.stem,
)
@freeze_time("2020-06-19 00:00:00+0000")
def test_generate_callbacks(oas_file: Path, output_dir: Path) -> None:
    run_cli_and_assert(
        input_path=oas_file,
        output_path=output_dir,
        expected_path=EXPECTED_OPENAPI_PATH / "coverage" / oas_file.stem,
    )


@pytest.mark.cli_doc(
    options=["--model-file"],
    option_description="Write generated models to a custom module path.",
    cli_args=[
        "--input",
        "openapi/default_template/body_and_parameters.yaml",
        "--output",
        "app",
        "--model-file",
        "custom_models.py",
        "--model-template-dir",
        "model_templates",
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--python-version",
        "3.13",
    ],
    input_schema="openapi/default_template/body_and_parameters.yaml",
    golden_output="openapi/coverage/model_options/custom_models.py",
    related_options=[
        "--model-template-dir",
        "--output-model-type",
        "--python-version",
    ],
)
@pytest.mark.cli_doc(
    options=["--model-template-dir"],
    option_description="Use a custom datamodel-code-generator template directory.",
    cli_args=[
        "--input",
        "openapi/default_template/body_and_parameters.yaml",
        "--output",
        "app",
        "--model-file",
        "custom_models.py",
        "--model-template-dir",
        "model_templates",
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--python-version",
        "3.13",
    ],
    input_schema="openapi/default_template/body_and_parameters.yaml",
    golden_output="openapi/coverage/model_options/custom_models.py",
    related_options=["--model-file", "--output-model-type", "--python-version"],
)
@pytest.mark.cli_doc(
    options=["--output-model-type"],
    option_description="Choose the datamodel-code-generator output backend.",
    cli_args=[
        "--input",
        "openapi/default_template/body_and_parameters.yaml",
        "--output",
        "app",
        "--model-file",
        "custom_models.py",
        "--model-template-dir",
        "model_templates",
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--python-version",
        "3.13",
    ],
    input_schema="openapi/default_template/body_and_parameters.yaml",
    golden_output="openapi/coverage/model_options/custom_models.py",
    related_options=["--model-file", "--model-template-dir", "--python-version"],
)
@pytest.mark.cli_doc(
    options=["--python-version"],
    option_description="Target a specific Python version when formatting generated code.",
    cli_args=[
        "--input",
        "openapi/default_template/body_and_parameters.yaml",
        "--output",
        "app",
        "--model-file",
        "custom_models.py",
        "--model-template-dir",
        "model_templates",
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--python-version",
        "3.13",
    ],
    input_schema="openapi/default_template/body_and_parameters.yaml",
    golden_output="openapi/coverage/model_options/custom_models.py",
    related_options=["--model-file", "--model-template-dir", "--output-model-type"],
)
@freeze_time("2020-06-19")
def test_generate_with_model_options(tmp_path: Path, output_dir: Path) -> None:
    model_template_root = tmp_path / "model_templates"
    model_template_dir = model_template_root / "pydantic_v2"
    model_template_dir.mkdir(parents=True)
    template_resource = files("datamodel_code_generator.model.template").joinpath(
        "pydantic_v2/BaseModel.jinja2"
    )
    with as_file(template_resource) as template_path:
        copy2(template_path, model_template_dir / "BaseModel.jinja2")
    run_cli_and_assert(
        input_path=DATA_PATH
        / OPEN_API_DEFAULT_TEMPLATE_DIR_NAME
        / "body_and_parameters.yaml",
        output_path=output_dir,
        expected_path=EXPECTED_OPENAPI_PATH / "coverage" / "model_options",
        extra_args=[
            "--model-file",
            "custom_models.py",
            "--model-template-dir",
            str(model_template_root),
            "--output-model-type",
            "pydantic_v2.BaseModel",
            "--python-version",
            "3.13",
        ],
    )


def test_invalid_custom_visitor(tmp_path: Path, output_dir: Path) -> None:
    visitor_path = tmp_path / "invalid_visitor.py"
    visitor_path.write_text("VALUE = 1\n", encoding="utf-8")
    with pytest.raises(Exception, match="does not have any visit function"):
        run_main_with_args(
            [
                "--input",
                str(DATA_PATH / OPEN_API_DEFAULT_TEMPLATE_DIR_NAME / "simple.yaml"),
                "--output",
                str(output_dir),
                "--custom-visitor",
                str(visitor_path),
            ]
        )


@pytest.mark.cli_doc(
    options=["--custom-visitor"],
    option_description="Load a custom visitor module and expose additional template variables.",
    cli_args=[
        "--input",
        "openapi/default_template/simple.yaml",
        "--output",
        "app",
        "--template-dir",
        "template",
        "--generate-routers",
        "--custom-visitor",
        "visitor.py",
    ],
    input_schema="openapi/default_template/simple.yaml",
)
def test_generate_routers_with_operations_without_tags(
    tmp_path: Path, output_dir: Path
) -> None:
    template_dir = tmp_path / "template"
    template_dir.mkdir()
    template_dir.joinpath("main.jinja2").write_text(
        "from fastapi import FastAPI\n\napp = FastAPI()\n",
        encoding="utf-8",
    )
    template_dir.joinpath("routers.jinja2").write_text(
        "from fastapi import APIRouter\n\nrouter = APIRouter()\n",
        encoding="utf-8",
    )
    visitor_path = tmp_path / "visitor.py"
    visitor_path.write_text(
        "\n".join(
            [
                "from types import SimpleNamespace",
                "",
                "def visit(parser, model_path):",
                "    del parser, model_path",
                "    return {'operations': [SimpleNamespace(path='/untagged')]}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    assert (
        run_main_with_args(
            [
                "--input",
                str(DATA_PATH / OPEN_API_DEFAULT_TEMPLATE_DIR_NAME / "simple.yaml"),
                "--output",
                str(output_dir),
                "--template-dir",
                str(template_dir),
                "--generate-routers",
                "--custom-visitor",
                str(visitor_path),
            ]
        )
        == 0
    )
    assert sorted(
        path.relative_to(output_dir) for path in output_dir.rglob("*") if path.is_file()
    ) == [
        Path("main.py"),
        Path("models.py"),
    ]
    validate_generated_code(output_dir)
