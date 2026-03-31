from pathlib import Path

from typer.testing import CliRunner

from fastapi_code_generator.__main__ import app

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "--input" in result.output
    assert "--output" in result.output


def test_cli_generate(tmp_path: Path):
    input_file = tmp_path / "api.yaml"
    output_dir = tmp_path / "generated"
    input_file.write_text(
        """\
openapi: 3.0.0
info:
  title: Basic
  version: 1.0.0
paths:
  /pets/{petId}:
    get:
      operationId: getPet
      parameters:
        - name: petId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: ok
""",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "--input",
            str(input_file),
            "--output",
            str(output_dir),
            "--disable-timestamp",
        ],
    )

    assert result.exit_code == 0
    assert (output_dir / "main.py").exists()
    assert (output_dir / "models.py").exists()
