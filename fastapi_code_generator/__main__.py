from datetime import datetime, timezone
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer
from datamodel_code_generator import LiteralType, PythonVersion, chdir
from datamodel_code_generator.format import CodeFormatter
from datamodel_code_generator.imports import Import, Imports
from datamodel_code_generator.reference import Reference
from datamodel_code_generator.types import DataType
from jinja2 import Environment, FileSystemLoader

from fastapi_code_generator.parser import OpenAPIParser
from fastapi_code_generator.visitor import Visitor

app = typer.Typer()

BUILTIN_TEMPLATE_DIR = Path(__file__).parent / "template"

BUILTIN_VISITOR_DIR = Path(__file__).parent / "visitors"

MODEL_PATH: Path = Path("models.py")


def dynamic_load_module(module_path: Path) -> Any:
    module_name = module_path.stem
    spec = spec_from_file_location(module_name, str(module_path))
    if spec:
        module = module_from_spec(spec)
        if spec.loader:
            spec.loader.exec_module(module)
            return module
    raise Exception(f"{module_name} can not be loaded")


@app.command()
def main(
    encoding: str = typer.Option("cp1252", "--encoding", "-e"),
    input_file: str = typer.Option(..., "--input", "-i"),
    output_dir: Path = typer.Option(..., "--output", "-o"),
    model_file: str = typer.Option(None, "--model-file", "-m"),
    template_dir: Optional[Path] = typer.Option(None, "--template-dir", "-t"),
    enum_field_as_literal: Optional[LiteralType] = typer.Option(
        None, "--enum-field-as-literal"
    ),
    custom_visitors: Optional[List[Path]] = typer.Option(
        None, "--custom-visitor", "-c"
    ),
    disable_timestamp: bool = typer.Option(False, "--disable-timestamp"),
) -> None:
    input_name: str = input_file
    input_text: str

    with open(input_file, encoding=encoding) as f:
        input_text = f.read()

    if model_file:
        model_path = Path(model_file).with_suffix('.py')
    else:
        model_path = MODEL_PATH
    if enum_field_as_literal:
        return generate_code(
            input_name,
            input_text,
            encoding,
            output_dir,
            template_dir,
            model_path,
            enum_field_as_literal,
            disable_timestamp=disable_timestamp,
        )
    return generate_code(
        input_name,
        input_text,
        encoding,
        output_dir,
        template_dir,
        model_path,
        custom_visitors=custom_visitors,
        disable_timestamp=disable_timestamp,
    )


def _get_most_of_reference(data_type: DataType) -> Optional[Reference]:
    if data_type.reference:
        return data_type.reference
    for data_type in data_type.data_types:
        reference = _get_most_of_reference(data_type)
        if reference:
            return reference
    return None


def generate_code(
    input_name: str,
    input_text: str,
    encoding: str,
    output_dir: Path,
    template_dir: Optional[Path],
    model_path: Optional[Path] = None,
    enum_field_as_literal: Optional[str] = None,
    custom_visitors: Optional[List[Path]] = [],
    disable_timestamp: bool = False,
) -> None:
    if not model_path:
        model_path = MODEL_PATH
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    if not template_dir:
        template_dir = BUILTIN_TEMPLATE_DIR
    if enum_field_as_literal:
        parser = OpenAPIParser(input_text, enum_field_as_literal=enum_field_as_literal)
    else:
        parser = OpenAPIParser(input_text)
    with chdir(output_dir):
        models = parser.parse()
    if not models:
        return
    elif isinstance(models, str):
        output = output_dir / model_path
        modules = {output: (models, input_name)}
    else:
        raise Exception('Modular references are not supported in this version')

    environment: Environment = Environment(
        loader=FileSystemLoader(
            template_dir if template_dir else f"{Path(__file__).parent}/template",
            encoding="utf8",
        ),
    )

    results: Dict[Path, str] = {}
    code_formatter = CodeFormatter(PythonVersion.PY_38, Path().resolve())

    template_vars: Dict[str, object] = {"info": parser.parse_info()}
    visitors: List[Visitor] = []

    # Load visitors
    builtin_visitors = BUILTIN_VISITOR_DIR.rglob("*.py")
    visitors_path = [*builtin_visitors, *(custom_visitors if custom_visitors else [])]
    for visitor_path in visitors_path:
        module = dynamic_load_module(visitor_path)
        if hasattr(module, "visit"):
            visitors.append(module.visit)
        else:
            raise Exception(f"{visitor_path.stem} does not have any visit function")

    # Call visitors to build template_vars
    for visitor in visitors:
        visitor_result = visitor(parser, model_path)
        template_vars = {**template_vars, **visitor_result}

    for target in template_dir.rglob("*"):
        relative_path = target.relative_to(template_dir)
        template = environment.get_template(str(relative_path))
        result = template.render(template_vars)
        results[relative_path] = code_formatter.format_code(result)

    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    header = f"""\
# generated by fastapi-codegen:
#   filename:  {Path(input_name).name}"""
    if not disable_timestamp:
        header += f"\n#   timestamp: {timestamp}"

    for path, code in results.items():
        with output_dir.joinpath(path.with_suffix(".py")).open("wt", encoding=encoding) as file:
            print(header, file=file)
            print("", file=file)
            print(code.rstrip(), file=file)

    header = f'''\
# generated by fastapi-codegen:
#   filename:  {{filename}}'''
    if not disable_timestamp:
        header += f'\n#   timestamp: {timestamp}'

    for path, body_and_filename in modules.items():
        body, filename = body_and_filename
        if path is None:
            file = None
        else:
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            file = path.open('wt', encoding='utf8')

        print(header.format(filename=filename), file=file)
        if body:
            print('', file=file)
            print(body.rstrip(), file=file)

        if file is not None:
            file.close()


if __name__ == "__main__":
    typer.run(main)
