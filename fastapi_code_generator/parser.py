from __future__ import annotations

import re
from contextvars import ContextVar
from functools import cached_property
from typing import Any, Dict, List, Optional, Union

import stringcase
from datamodel_code_generator import (
    DataModelField,
    load_json_or_yaml,
    snooper_to_methods,
)
from datamodel_code_generator.imports import IMPORT_LIST, Import, Imports
from datamodel_code_generator.model.pydantic.types import type_map
from datamodel_code_generator.parser.jsonschema import (
    JsonSchemaObject,
    json_schema_data_formats,
)
from datamodel_code_generator.types import DataType
from pydantic import BaseModel, validator
from pydantic.fields import ModelField

MODEL_PATH = ".models"

model_path_var: ContextVar[str] = ContextVar('model_path', default=MODEL_PATH)


class CachedPropertyModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        keep_untouched = (cached_property,)


class Response(BaseModel):
    status_code: str
    description: Optional[str]
    contents: Dict[str, JsonSchemaObject]


class Request(BaseModel):
    description: Optional[str]
    contents: Dict[str, JsonSchemaObject]
    required: bool


class UsefulStr(str):
    @property
    def snakecase(self) -> str:
        return stringcase.snakecase(self)

    @property
    def pascalcase(self) -> str:
        return stringcase.pascalcase(self)

    @property
    def camelcase(self) -> str:
        return stringcase.camelcase(self)


class Argument(BaseModel):
    name: UsefulStr

    @validator('name')
    def validate_name(cls, value: Any) -> Any:
        if type(value) == str:
            return UsefulStr(value)
        return value

    # def __str__(self) -> UsefulStr:
    #     return self.name


class Operation(CachedPropertyModel):
    type: Optional[UsefulStr]
    path: Optional[UsefulStr]
    operationId: Optional[UsefulStr]
    root_path: Optional[UsefulStr]
    parameters: Optional[Any]
    responses: Dict[UsefulStr, Any] = {}
    requestBody: Dict[UsefulStr, Any] = {}
    imports: List[Import] = []

    @cached_property
    def snake_case_path(self) -> str:
        return re.sub(  # type: ignore
            r"{([^\}]+)}", lambda m: stringcase.snakecase(m.group()), self.path
        )

    def set_path(self, path: Path) -> None:
        self.path = path.path
        self.root_path = UsefulStr(path.root_path)

    @cached_property
    def request(self) -> Optional[str]:
        models: List[str] = []
        for requests in self.request_objects:
            for content_type, schema in requests.contents.items():
                if content_type == "application/json":
                    models.append(schema.ref_object_name)
                    self.imports.append(
                        Import(
                            from_=model_path_var.get(), import_=schema.ref_object_name
                        )
                    )
        if not models:
            return None
        if len(models) > 1:
            return f'Union[{",".join(models)}]'
        return models[0]

    @cached_property
    def request_objects(self) -> List[Request]:
        requests: List[Request] = []
        contents: Dict[str, JsonSchemaObject] = {}
        for content_type, obj in self.requestBody.get("content", {}).items():
            contents[content_type] = (
                JsonSchemaObject.parse_obj(obj["schema"]) if "schema" in obj else None
            )
            requests.append(
                Request(
                    description=self.requestBody.get("description"),
                    contents=contents,
                    required=self.requestBody.get("required") == "true",
                )
            )
        return requests

    @cached_property
    def response_objects(self) -> List[Response]:
        responses: List[Response] = []
        for status_code, detail in self.responses.items():
            contents = {}
            for content_type, obj in detail.get("content", {}).items():
                contents[content_type] = (
                    JsonSchemaObject.parse_obj(obj["schema"])
                    if "schema" in obj
                    else None
                )

            responses.append(
                Response(
                    status_code=status_code,
                    description=detail.get("description"),
                    contents=contents,
                )
            )
        return responses

    @cached_property
    def function_name(self) -> str:
        if self.operationId:
            name: str = self.operationId
        else:
            name = f"{self.type}{self.path.replace('/', '_')}"  # type: ignore
        return stringcase.snakecase(name)

    @property
    def dump_imports(self) -> str:
        imports = Imports()
        imports.append(self.imports)
        return imports.dump()

    @cached_property
    def arguments(self) -> str:
        return self.get_arguments(snake_case=False)

    @cached_property
    def snake_case_arguments(self) -> str:
        return self.get_arguments(snake_case=True)

    def get_arguments(self, snake_case: bool) -> str:
        arguments: List[str] = []

        if self.parameters:
            for parameter in self.parameters:
                arguments.append(self.get_parameter_type(parameter, snake_case))

        if self.request:
            arguments.append(f"body: {self.request}")

        return ", ".join(arguments)

    @cached_property
    def argument_list(self) -> List[Argument]:
        arguments: List[Argument] = []

        if self.parameters:
            for parameter in self.parameters:
                arguments.append(Argument.parse_obj(parameter))

        if self.request:
            arguments.append(Argument(name='body'))

        return arguments

    def get_parameter_type(
        self, parameter: Dict[str, Union[str, Dict[str, str]]], snake_case: bool
    ) -> str:
        format_ = parameter["schema"].get("format", "default")  # type: ignore
        type_ = json_schema_data_formats[parameter["schema"]["type"]][format_]  # type: ignore
        return self.get_data_type_hint(
            name=stringcase.snakecase(parameter["name"])
            if snake_case
            else parameter["name"],
            data_types=[type_map[type_]],
            required=parameter.get("required") == "true"
            or parameter.get("in") == "path",
            snake_case=snake_case,
        )

    def get_data_type_hint(
        self,
        name: str,
        data_types: List[DataType],
        required: bool,
        snake_case: bool,
        default: Optional[str] = None,
        auto_import: bool = True,
    ) -> str:
        field = DataModelField(
            name=stringcase.snakecase(name) if snake_case else name,
            data_types=data_types,
            required=required,
            default=default,
        )
        if auto_import:
            self.imports.extend(field.imports)

        if not default and field.required:
            return f"{field.name}: {field.type_hint}"
        return f'{field.name}: {field.type_hint} = {default or "None"}'

    @cached_property
    def response(self) -> str:
        models: List[str] = []
        for response in self.response_objects:
            # expect 2xx
            if response.status_code.startswith("2"):
                for content_type, schema in response.contents.items():
                    if content_type == "application/json":
                        if schema.is_array:
                            if isinstance(schema.items, JsonSchemaObject):
                                type_ = f'List[{schema.items.ref_object_name}]'
                                self.imports.append(
                                    Import(
                                        from_=model_path_var.get(),
                                        import_=schema.items.ref_object_name,
                                    )
                                )
                            else:
                                type_ = f'List[{",".join(i.ref_object_name for i in schema.items)}]'
                                self.imports.extend(
                                    Import(
                                        from_=model_path_var.get(),
                                        import_=i.ref_object_name,
                                    )
                                    for i in schema.items
                                )
                            self.imports.append(IMPORT_LIST)
                        else:
                            type_ = schema.ref_object_name
                            self.imports.append(
                                Import(
                                    from_=model_path_var.get(),
                                    import_=schema.ref_object_name,
                                )
                            )
                        models.append(type_)

        if not models:
            return "None"
        if len(models) > 1:
            return f'Union[{",".join(models)}]'
        return models[0]


OPERATION_NAMES: List[str] = [
    "get",
    "put",
    "post",
    "delete",
    "patch",
    "head",
    "options",
    "trace",
]


class Operations(BaseModel):
    parameters: Optional[Any] = None
    get: Optional[Operation] = None
    put: Optional[Operation] = None
    post: Optional[Operation] = None
    delete: Optional[Operation] = None
    patch: Optional[Operation] = None
    head: Optional[Operation] = None
    options: Optional[Operation] = None
    trace: Optional[Operation] = None

    @validator(*OPERATION_NAMES)
    def validate_operations(cls, value: Any, field: ModelField) -> Any:
        if isinstance(value, Operation):
            value.type = field.name
        return value


class Path(BaseModel):
    path: Optional[str]
    operations: Optional[Operations] = None
    children: List[Path] = []
    parent: Optional[Path] = None

    @property
    def exists_operations(self) -> List[Operation]:
        return [
            operation
            for operation_name in OPERATION_NAMES
            if (operation := getattr(self.operations, operation_name))
        ]

    @property
    def root_path(self) -> str:
        paths = self.path.split("/")  # type: ignore
        if len(paths) > 1:
            return paths[1]
        else:
            return ""

    def init(self) -> None:
        if self.parent:
            self.parent.children.append(self)


Path.update_forward_refs()


class ParsedObject:
    def __init__(self, parsed_operations: List[Operation]):
        self.operations: List[Operation] = sorted(
            parsed_operations, key=lambda m: m.path
        )
        self.imports: Imports = Imports()
        for operation in self.operations:
            # create imports
            operation.arguments
            operation.request
            operation.response
            self.imports.append(operation.imports)


@snooper_to_methods(max_variable_length=None)
class OpenAPIParser:
    def __init__(
        self, input_name: str, input_text: str, model_path: Optional[str] = None
    ) -> None:
        self.input_name: str = input_name
        self.input_text: str = input_text
        if model_path:
            model_path_var.set(model_path)

    def parse(self) -> ParsedObject:
        openapi = load_json_or_yaml(self.input_text)
        return self.parse_paths(openapi["paths"])

    def parse_paths(self, path_tree: Dict[str, Any]) -> ParsedObject:
        paths: List[Path] = []
        for path_name, operations in path_tree.items():
            tree: List[str] = []
            last: Optional[Path] = None

            for key in path_name.split("/"):
                parent: Optional[Path] = None
                parents = [p for p in paths if p.path == "/".join(tree)]
                if parents:
                    parent = parents[0]

                tree.append(key)

                me = [p for p in paths if p.path == "/".join(tree)]

                if me:
                    continue

                last = Path(path="/".join(tree), parent=parent)

                paths.append(last)

            if last:
                last.operations = Operations.parse_obj(operations)

        for path in paths:
            path.init()

        parsed_operations: List[Operation] = []
        for path in paths:
            for child in path.children:
                parsed_operations.extend(self.parse_operation(child))
        return ParsedObject(parsed_operations)

    @classmethod
    def parse_operation(cls, path: Path) -> List[Operation]:
        operations: List[Operation] = []
        if path.operations:
            for operation in path.exists_operations:
                operation.set_path(path)
                if path.operations.parameters:
                    if operation.parameters:
                        operation.parameters.extend(path.operations.parameters)
                    else:
                        operation.parameters = path.operations.parameters

                operations.append(operation)
        return operations
