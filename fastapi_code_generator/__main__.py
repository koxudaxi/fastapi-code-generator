import re
from datetime import datetime, timezone
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer
from datamodel_code_generator import DataModelType, LiteralType, PythonVersion, chdir
from datamodel_code_generator.format import CodeFormatter
from datamodel_code_generator.imports import Import, Imports
from datamodel_code_generator.model import get_data_model_types
from datamodel_code_generator.reference import Reference
from datamodel_code_generator.types import DataType
from jinja2 import Environment, FileSystemLoader

from fastapi_code_generator.parser import OpenAPIParser
from fastapi_code_generator.visitor import Visitor

app = typer.Typer()

all_tags = []

TITLE_PATTERN = re.compile(r'(?<!^)(?<![A-Z ])(?=[A-Z])| ')

BUILTIN_MODULAR_TEMPLATE_DIR = Path(__file__).parent / "modular_template"

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
    encoding: str = typer.Option("utf-8", "--encoding", "-e"),
    input_file: str = typer.Option(..., "--input", "-i"),
    output_dir: Path = typer.Option(..., "--output", "-o"),
    model_file: str = typer.Option(None, "--model-file", "-m"),
    template_dir: Optional[Path] = typer.Option(None, "--template-dir", "-t"),
    enum_field_as_literal: Optional[LiteralType] = typer.Option(
        None, "--enum-field-as-literal"
    ),
    generate_routers: bool = typer.Option(False, "--generate-routers", "-r"),
    specify_tags: Optional[str] = typer.Option(None, "--specify-tags"),
    custom_visitors: Optional[List[Path]] = typer.Option(
        None, "--custom-visitor", "-c"
    ),
    disable_timestamp: bool = typer.Option(False, "--disable-timestamp"),
    output_model_type: DataModelType = typer.Option(
        DataModelType.PydanticBaseModel.value, "--output-model-type", "-d"
    ),
    python_version: PythonVersion = typer.Option(
        PythonVersion.PY_38.value, "--python-version", "-p"
    ),
) -> None:
    input_name: str = input_file
    input_text: str

    with open(input_file, encoding=encoding) as f:
        input_text = f.read()

    if model_file:
        model_path = Path(model_file).with_suffix('.py')
    else:
        model_path = MODEL_PATH

    return generate_code(
        input_name,
        input_text,
        encoding,
        output_dir,
        template_dir,
        model_path,
        enum_field_as_literal=enum_field_as_literal or None,
        custom_visitors=custom_visitors,
        disable_timestamp=disable_timestamp,
        generate_routers=generate_routers,
        specify_tags=specify_tags,
        output_model_type=output_model_type,
        python_version=python_version,
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
    enum_field_as_literal: Optional[LiteralType] = None,
    custom_visitors: Optional[List[Path]] = None,
    disable_timestamp: bool = False,
    generate_routers: Optional[bool] = None,
    specify_tags: Optional[str] = None,
    output_model_type: DataModelType = DataModelType.PydanticBaseModel,
    python_version: PythonVersion = PythonVersion.PY_38,
) -> None:
    if not model_path:
        model_path = MODEL_PATH
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    if generate_routers:
        Path(output_dir / "routers").mkdir(parents=True, exist_ok=True)
    if not template_dir:
        template_dir = (
            BUILTIN_MODULAR_TEMPLATE_DIR if generate_routers else BUILTIN_TEMPLATE_DIR
        )
    if not custom_visitors:
        custom_visitors = []
    data_model_types = get_data_model_types(output_model_type, python_version)

    parser = OpenAPIParser(
        input_text,
        enum_field_as_literal=enum_field_as_literal,
        data_model_type=data_model_types.data_model,
        data_model_root_type=data_model_types.root_model,
        data_model_field_type=data_model_types.field_model,
        data_type_manager_type=data_model_types.data_type_manager,
        dump_resolve_reference_action=data_model_types.dump_resolve_reference_action,
        target_python_version=python_version,
    )

    with chdir(output_dir):
        models = parser.parse()
    output = output_dir / model_path
    if not models:
        # if no models (schemas), just generate an empty model file.
        modules = {output: ("", input_name)}
    elif isinstance(models, str):
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
    code_formatter = CodeFormatter(python_version, Path().resolve())

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

    if generate_routers:
        operations: Any = template_vars.get("operations", [])
        for operation in operations:
            if hasattr(operation, "tags"):
                for tag in operation.tags:
                    all_tags.append(tag)
    # Convert from Tag Names to router_names
    sorted_tags = sorted(set(all_tags), key=lambda x: x.lower())
    routers = sorted(
        [re.sub(TITLE_PATTERN, '_', tag.strip()).lower() for tag in sorted_tags]
    )
    template_vars = {**template_vars, "routers": routers, "tags": sorted_tags}

    for target in template_dir.rglob("*"):
        relative_path = target.relative_to(template_dir)
        template = environment.get_template(str(relative_path))
        result = template.render(template_vars)
        results[relative_path] = code_formatter.format_code(result)

    if generate_routers:
        tags = sorted_tags
        results.pop(Path("routers.jinja2"))
        if specify_tags:
            if Path(output_dir.joinpath("main.py")).exists():
                with open(Path(output_dir.joinpath("main.py")), 'r') as file:
                    content = file.read()
                    if "app.include_router" in content:
                        tags = sorted(
                            set(tag.strip() for tag in str(specify_tags).split(","))
                        )

        for target in template_dir.rglob("routers.*"):
            relative_path = target.relative_to(template_dir)
            for router, tag in zip(routers, sorted_tags):
                if (
                    not Path(output_dir.joinpath("routers", router))
                    .with_suffix(".py")
                    .exists()
                    or tag in tags
                ):
                    template_vars["tag"] = tag.strip()
                    template = environment.get_template(str(relative_path))
                    result = template.render(template_vars)
                    router_path = Path("routers", router).with_suffix(".jinja2")
                    results[router_path] = code_formatter.format_code(result)

    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    header = f"""\
# generated by fastapi-codegen:
#   filename:  {Path(input_name).name}"""
    if not disable_timestamp:
        header += f"\n#   timestamp: {timestamp}"

    for path, code in results.items():
        with output_dir.joinpath(path.with_suffix(".py")).open(
            "wt", encoding=encoding
        ) as file:
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
