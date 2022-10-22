from pathlib import Path
from typing import Dict, List

from fastapi_code_generator.parser import OpenAPIParser, Operation
from fastapi_code_generator.visitor import Visitor


def get_operations(parser: OpenAPIParser, model_path: Path) -> Dict[str, object]:
    sorted_operations: List[Operation] = sorted(
        parser.operations.values(), key=lambda m: m.path
    )
    return {'operations': sorted_operations}


visit: Visitor = get_operations
