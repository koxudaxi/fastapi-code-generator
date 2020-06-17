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
from pydantic import BaseModel, root_validator

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
    @classmethod
    def __get_validators__(cls) -> Any:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> Any:
        return cls(v)

    @property
    def snakecase(self) -> str:
        return stringcase.snakecase(self)

    @property
    def pascalcase(self) -> str:
        return stringcase.pascalcase(self)

    @property
    def camelcase(self) -> str:
        return stringcase.camelcase(self)


class Argument(CachedPropertyModel):
    name: UsefulStr
    type_hint: UsefulStr
    default: Optional[UsefulStr]
    required: bool

    def __str__(self) -> str:
        return self.argument

    @cached_property
    def argument(self) -> str:
        if not self.default and self.required:
            return f'{self.name}: {self.type_hint}'
        return f'{self.name}: {self.type_hint} = {self.default}'


class Operation(CachedPropertyModel):
    type: UsefulStr
    path: UsefulStr
    operationId: Optional[UsefulStr]
    parameters: List[Dict[str, Any]] = []
    responses: Dict[UsefulStr, Any] = {}
    requestBody: Dict[str, Any] = {}
    imports: List[Import] = []

    @cached_property
    def root_path(self) -> UsefulStr:
        paths = self.path.split("/")
        return UsefulStr(paths[1] if len(paths) > 1 else '')

    @cached_property
    def snake_case_path(self) -> str:
        return re.sub(
            r"{([^\}]+)}", lambda m: stringcase.snakecase(m.group()), self.path
        )

    @cached_property
    def request(self) -> Optional[Argument]:
        arguments: List[Argument] = []
        for requests in self.request_objects:
            for content_type, schema in requests.contents.items():
                # TODO: support other content-types
                if content_type == "application/json":
                    arguments.append(
                        # TODO: support multiple body
                        Argument(
                            name='body',  # type: ignore
                            type_hint=schema.ref_object_name,  # type: ignore
                            required=requests.required,
                        )
                    )
                    self.imports.append(
                        Import(
                            from_=model_path_var.get(), import_=schema.ref_object_name
                        )
                    )
        if not arguments:
            return None
        return arguments[0]

    @cached_property
    def request_objects(self) -> List[Request]:
        requests: List[Request] = []
        contents: Dict[str, JsonSchemaObject] = {}
        for content_type, obj in self.requestBody.get('content', {}).items():
            contents[content_type] = (
                JsonSchemaObject.parse_obj(obj['schema']) if 'schema' in obj else None
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
            name = f"{self.type}{self.path.replace('/', '_')}"
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
        return ", ".join(
            argument.argument for argument in self.get_argument_list(snake_case)
        )

    @cached_property
    def argument_list(self) -> List[Argument]:
        return self.get_argument_list(False)

    def get_argument_list(self, snake_case: bool) -> List[Argument]:
        arguments: List[Argument] = []

        if self.parameters:
            for parameter in self.parameters:
                arguments.append(self.get_parameter_type(parameter, snake_case))

        if self.request:
            arguments.append(self.request)
        return arguments

    def get_parameter_type(
        self, parameter: Dict[str, Union[str, Dict[str, str]]], snake_case: bool
    ) -> Argument:
        schema: JsonSchemaObject = JsonSchemaObject.parse_obj(parameter["schema"])
        format_ = schema.format or "default"
        type_ = json_schema_data_formats[schema.type][format_]
        name: str = parameter["name"]

        field = DataModelField(
            name=stringcase.snakecase(name) if snake_case else name,
            data_types=[type_map[type_]],
            required=parameter.get("required") == "true"
            or parameter.get("in") == "path",
            default=schema.typed_default,
        )
        self.imports.extend(field.imports)
        return Argument(
            name=field.name,  # type: ignore
            type_hint=field.type_hint,  # type: ignore
            default=field.default,  # type: ignore
            required=field.required,  # type: ignore
        )

    @cached_property
    def response(self) -> str:
        models: List[str] = []
        for response in self.response_objects:
            # expect 2xx
            if response.status_code.startswith("2"):
                for content_type, schema in response.contents.items():
                    if content_type == "application/json":
                        if schema.is_array:
                            if isinstance(schema.items, list):
                                type_ = f'List[{",".join(i.ref_object_name for i in schema.items)}]'
                                self.imports.extend(
                                    Import(
                                        from_=model_path_var.get(),
                                        import_=i.ref_object_name,
                                    )
                                    for i in schema.items
                                )
                            else:
                                type_ = f'List[{schema.items.ref_object_name}]'
                                self.imports.append(
                                    Import(
                                        from_=model_path_var.get(),
                                        import_=schema.items.ref_object_name,
                                    )
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
    parameters: List[Dict[str, Any]] = []
    get: Optional[Operation] = None
    put: Optional[Operation] = None
    post: Optional[Operation] = None
    delete: Optional[Operation] = None
    patch: Optional[Operation] = None
    head: Optional[Operation] = None
    options: Optional[Operation] = None
    trace: Optional[Operation] = None
    path: UsefulStr

    @root_validator(pre=True)
    def inject_path_and_type_to_operation(cls, values: Dict[str, Any]) -> Any:
        path: Any = values.get('path')
        return dict(
            **{
                o: dict(**v, path=path, type=o)
                for o in OPERATION_NAMES
                if (v := values.get(o))
            },
            path=path,
            parameters=values.get('parameters', []),
        )

    @root_validator
    def inject_parameters_to_operation(cls, values: Dict[str, Any]) -> Any:
        if parameters := values.get('parameters'):
            for operation_name in OPERATION_NAMES:
                if operation := values.get(operation_name):
                    operation.parameters.extend(parameters)
        return values


class Path(CachedPropertyModel):
    path: UsefulStr
    operations: Optional[Operations] = None

    @root_validator(pre=True)
    def validate_root(cls, values: Dict[str, Any]) -> Any:
        if path := values.get('path'):
            if isinstance(path, str):
                if operations := values.get('operations'):
                    if isinstance(operations, dict):
                        return {
                            'path': path,
                            'operations': dict(**operations, path=path),
                        }
        return values

    @cached_property
    def exists_operations(self) -> List[Operation]:
        if self.operations:
            return [
                operation
                for operation_name in OPERATION_NAMES
                if (operation := getattr(self.operations, operation_name))
            ]
        return []


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

    def parse_paths(self, paths: Dict[str, Any]) -> ParsedObject:
        return ParsedObject(
            [
                operation
                for path_name, operations in paths.items()
                for operation in Path(
                    path=UsefulStr(path_name), operations=operations
                ).exists_operations
            ]
        )
