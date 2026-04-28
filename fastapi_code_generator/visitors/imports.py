import re
from pathlib import Path
from typing import Dict, Optional

from datamodel_code_generator.imports import Import, Imports
from datamodel_code_generator.reference import Reference
from datamodel_code_generator.types import DataType

from fastapi_code_generator.parser import OpenAPIParser
from fastapi_code_generator.visitor import Visitor

IDENTIFIER_PATTERN = re.compile(r'\b[A-Za-z_][A-Za-z0-9_]*\b')


def _get_most_of_reference(data_type: DataType) -> Optional[Reference]:
    if data_type.reference:
        return data_type.reference
    for data_type in data_type.data_types:
        reference = _get_most_of_reference(data_type)
        if reference:
            return reference
    return None


def _collect_used_names(parser: OpenAPIParser) -> set[str]:
    names: set[str] = set()
    pending_operations = list(parser.operations.values())
    while pending_operations:
        operation = pending_operations.pop()
        names.update(IDENTIFIER_PATTERN.findall(operation.arguments))
        names.update(IDENTIFIER_PATTERN.findall(operation.return_type))
        names.update(IDENTIFIER_PATTERN.findall(operation.response))
        for models in operation.additional_responses.values():
            for model in models.values():
                names.update(IDENTIFIER_PATTERN.findall(model))
        for callback_operations in operation.callbacks.values():
            pending_operations.extend(callback_operations)
    return names


def _remove_unused_imports(imports: Imports, used_names: set[str]) -> None:
    unused = [
        (from_, import_)
        for from_, imports_ in imports.items()
        for import_ in imports_
        if not {imports.get_effective_name(from_, import_), import_}.intersection(
            used_names
        )
    ]
    reverse_lookup = {
        (import_.from_, import_.import_): reference_path
        for reference_path, import_ in imports.reference_paths.items()
    }
    for from_, import_ in unused:
        import_obj = Import(
            from_=from_,
            import_=import_,
            alias=imports.alias.get(from_, {}).get(import_),
            reference_path=reverse_lookup.get((from_, import_)),
        )
        while imports.counter.get((from_, import_), 0) > 0:
            imports.remove(import_obj)


def get_imports(parser: OpenAPIParser, model_path: Path) -> Dict[str, object]:
    imports = Imports()

    imports.update(parser.imports)
    for data_type in parser.data_types:
        reference = _get_most_of_reference(data_type)
        if reference:
            imports.append(data_type.all_imports)
            imports.append(
                Import.from_full_path(f'.{model_path.stem}.{reference.name}')
            )
    for from_, imports_ in parser.imports_for_fastapi.items():
        imports[from_].update(imports_)
    for operation in parser.operations.values():
        if operation.imports:
            imports.alias.update(operation.imports.alias)
    _remove_unused_imports(imports, _collect_used_names(parser))
    return {'imports': imports}


visit: Visitor = get_imports
