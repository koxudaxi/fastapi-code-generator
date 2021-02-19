from __future__ import annotations

import pathlib
import re
from contextvars import ContextVar
from typing import Any, Dict, List, Optional, Pattern, Union

import stringcase
from datamodel_code_generator import (
    DataModelField,
    cached_property,
    load_yaml,
    snooper_to_methods,
)
from datamodel_code_generator.imports import Import, Imports
from datamodel_code_generator.parser.jsonschema import (
    JsonSchemaObject,
    get_model_by_path,
)
from datamodel_code_generator.parser.openapi import OpenAPIParser as OpenAPIModelParser
from datamodel_code_generator.types import DataType
from pydantic import BaseModel, root_validator

MODEL_PATH: pathlib.Path = pathlib.Path("models.py")

model_module_name_var: ContextVar[str] = ContextVar(
    'model_module_name', default=f'.{MODEL_PATH.stem}'
)

RE_APPLICATION_JSON_PATTERN: Pattern[str] = re.compile(r'^application/.*json$')


def get_ref_body(
    ref: str, openapi_model_parser: OpenAPIModelParser, components: Dict[str, Any]
) -> Dict[str, Any]:
    if ref.startswith('#/components'):
        return get_model_by_path(components, ref[13:].split('/'))
    elif ref.startswith('http://') or ref.startswith('https://'):
        if '#/' in ref:
            url, path = ref.rsplit('#/', 1)
            ref_body = openapi_model_parser._get_ref_body(url)
            return get_model_by_path(ref_body, path.split('/'))
        else:
            return openapi_model_parser._get_ref_body(ref)
    raise NotImplementedError(f'ref={ref} is not supported')


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
    default_value: Optional[UsefulStr]
    required: bool

    def __str__(self) -> str:
        return self.argument

    @cached_property
    def argument(self) -> str:
        if self.default is None and self.required:
            return f'{self.name}: {self.type_hint}'
        return f'{self.name}: {self.type_hint} = {self.default}'


class Operation(CachedPropertyModel):
    type: UsefulStr
    path: UsefulStr
    operationId: Optional[UsefulStr]
    summary: Optional[str]
    parameters: List[Dict[str, Any]] = []
    responses: Dict[UsefulStr, Any] = {}
    requestBody: Dict[str, Any] = {}
    imports: List[Import] = []
    security: Optional[List[Dict[str, List[str]]]] = None
    components: Dict[str, Any] = {}
    openapi_model_parser: OpenAPIModelParser

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
                if RE_APPLICATION_JSON_PATTERN.match(content_type):
                    data_type = self.get_data_type(schema, 'request')
                    arguments.append(
                        # TODO: support multiple body
                        Argument(
                            name='body',  # type: ignore
                            type_hint=data_type.type_hint,
                            required=requests.required,
                        )
                    )
                    self.imports.extend(data_type.imports_)

        if not arguments:
            return None
        return arguments[0]

    @cached_property
    def request_objects(self) -> List[Request]:
        requests: List[Request] = []
        contents: Dict[str, JsonSchemaObject] = {}
        ref: Optional[str] = self.requestBody.get('$ref')
        if ref:
            request_body = get_ref_body(ref, self.openapi_model_parser, self.components)
        else:
            request_body = self.requestBody
        for content_type, obj in request_body.get('content', {}).items():
            contents[content_type] = (
                JsonSchemaObject.parse_obj(obj['schema']) if 'schema' in obj else None
            )
            requests.append(
                Request(
                    description=request_body.get("description"),
                    contents=contents,
                    required=request_body.get("required") is True,
                )
            )
        return requests

    @cached_property
    def response_objects(self) -> List[Response]:
        responses: List[Response] = []
        for status_code, detail in self.responses.items():
            ref: Optional[str] = detail.get('$ref')
            if ref:
                ref_body = get_ref_body(ref, self.openapi_model_parser, self.components)
                content = ref_body.get("content", {})
                description = ref_body.get("description")
            else:
                content = detail.get("content", {})
                description = detail.get("description")
            contents = {}
            for content_type, obj in content.items():
                contents[content_type] = (
                    JsonSchemaObject.parse_obj(obj["schema"])
                    if "schema" in obj
                    else None
                )

            responses.append(
                Response(
                    status_code=status_code, description=description, contents=contents,
                )
            )
        return responses

    @cached_property
    def function_name(self) -> str:
        if self.operationId:
            name: str = self.operationId
        else:
            path = re.sub(r'/{|/', '_', self.snake_case_path).replace('}', '')
            name = f"{self.type}{path}"
        return stringcase.snakecase(name)

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

    def get_data_type(self, schema: JsonSchemaObject, suffix: str = '') -> DataType:
        if schema.ref:
            data_type = self.openapi_model_parser.get_ref_data_type(schema.ref)
            data_type.imports_.append(
                Import(
                    # TODO: Improve import statements
                    from_=model_module_name_var.get(),
                    import_=data_type.type,
                )
            )
            return data_type
        elif schema.is_array:
            # TODO: Improve handling array
            items = schema.items if isinstance(schema.items, list) else [schema.items]
            return self.openapi_model_parser.data_type(
                data_types=[self.get_data_type(i, suffix) for i in items], is_list=True
            )
        elif schema.is_object:
            camelcase_path = stringcase.camelcase(self.path[1:].replace("/", "_"))
            capitalized_suffix = suffix.capitalize()
            name: str = f'{camelcase_path}{self.type.capitalize()}{capitalized_suffix}'
            path = ['paths', self.path, self.type, capitalized_suffix]

            data_type = self.openapi_model_parser.parse_object(name, schema, path)

            self.imports.append(
                Import(from_=model_module_name_var.get(), import_=data_type.type,)
            )
            return data_type

        return self.openapi_model_parser.get_data_type(schema)

    def get_parameter_type(
        self, parameter: Dict[str, Union[str, Dict[str, str]]], snake_case: bool
    ) -> Argument:
        ref: Optional[str] = parameter.get('$ref')  # type: ignore
        if ref:
            parameter = get_ref_body(ref, self.openapi_model_parser, self.components)
        name: str = parameter["name"]  # type: ignore
        orig_name = name
        if snake_case:
            name = stringcase.snakecase(name)
        schema: JsonSchemaObject = JsonSchemaObject.parse_obj(parameter["schema"])

        field = DataModelField(
            name=name,
            data_type=self.get_data_type(schema, 'parameter'),
            required=parameter.get("required") or parameter.get("in") == "path",
        )
        self.imports.extend(field.imports)
        if orig_name != name:
            default: Optional[
                str
            ] = f"Query({'...' if field.required else repr(schema.default)}, alias='{orig_name}')"
            self.imports.append(Import(from_='fastapi', import_='Query'))
        else:
            default = repr(schema.default) if 'default' in parameter["schema"] else None
        return Argument(
            name=field.name,
            type_hint=field.type_hint,
            default=default,  # type: ignore
            default_value=schema.default,
            required=field.required,
        )

    @cached_property
    def response(self) -> str:
        data_types: List[DataType] = []
        for response in self.response_objects:
            # expect 2xx
            if response.status_code.startswith("2"):
                for content_type, schema in response.contents.items():
                    if RE_APPLICATION_JSON_PATTERN.match(content_type):
                        data_type = self.get_data_type(schema, 'response')
                        data_types.append(data_type)
                        self.imports.extend(data_type.imports_)

        if not data_types:
            return "None"
        if len(data_types) > 1:
            return self.openapi_model_parser.data_type(data_types=data_types).type_hint
        return data_types[0].type_hint


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
    class Config:
        arbitrary_types_allowed = (OpenAPIModelParser,)

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
    security: Optional[List[Dict[str, List[str]]]] = []
    components: Dict[str, Any] = {}
    openapi_model_parser: OpenAPIModelParser

    @root_validator(pre=True)
    def inject_path_and_type_to_operation(cls, values: Dict[str, Any]) -> Any:
        path: Any = values.get('path')
        openapi_model_parser: OpenAPIModelParser = values.get('openapi_model_parser')
        return dict(
            **{
                o: dict(
                    **values[o],
                    path=path,
                    type=o,
                    components=values.get('components', {}),
                    openapi_model_parser=openapi_model_parser,
                )
                for o in OPERATION_NAMES
                if o in values
            },
            path=path,
            parameters=values.get('parameters', []),
            security=values.get('security'),
            components=values.get('components', {}),
            openapi_model_parser=openapi_model_parser,
        )

    @root_validator
    def inject_parameters_and_security_to_operation(cls, values: Dict[str, Any]) -> Any:
        security = values.get('security')
        for operation_name in OPERATION_NAMES:
            operation = values.get(operation_name)
            if operation:
                parameters = values.get('parameters')
                if parameters:
                    operation.parameters.extend(parameters)
                if security is not None and operation.security is None:
                    operation.security = security

        return values


class Path(CachedPropertyModel):
    path: UsefulStr
    operations: Optional[Operations] = None
    security: Optional[List[Dict[str, List[str]]]] = []
    components: Dict[str, Any] = {}
    openapi_model_parser: OpenAPIModelParser

    @root_validator(pre=True)
    def validate_root(cls, values: Dict[str, Any]) -> Any:
        path = values.get('path')
        if path:
            if isinstance(path, str):
                operations = values.get('operations')
                if operations:
                    if isinstance(operations, dict):
                        security = values.get('security', [])
                        components = values.get('components', {})
                        openapi_model_parser = values.get('openapi_model_parser')
                        return {
                            'path': path,
                            'operations': dict(
                                **operations,
                                path=path,
                                security=security,
                                components=components,
                                openapi_model_parser=openapi_model_parser,
                            ),
                            'security': security,
                            'components': components,
                            'openapi_model_parser': openapi_model_parser,
                        }
        return values

    @cached_property
    def exists_operations(self) -> List[Operation]:
        if self.operations:
            return [
                getattr(self.operations, operation_name)
                for operation_name in OPERATION_NAMES
                if getattr(self.operations, operation_name)
            ]
        return []


Path.update_forward_refs()


class ParsedObject:
    def __init__(
        self,
        parsed_operations: List[Operation],
        info: Optional[List[Dict[str, Any]]] = None,
    ):
        self.operations: List[Operation] = sorted(
            parsed_operations, key=lambda m: m.path
        )
        self.imports: Imports = Imports()
        self.info = info
        for operation in self.operations:
            # create imports
            operation.arguments
            operation.snake_case_arguments
            operation.request
            operation.response
            self.imports.append(operation.imports)


@snooper_to_methods(max_variable_length=None)
class OpenAPIParser:
    def __init__(
        self,
        input_name: str,
        input_text: str,
        openapi_model_parser: Optional[OpenAPIModelParser] = None,
        model_module_name: Optional[str] = None,
    ) -> None:
        self.input_name: str = input_name
        self.input_text: str = input_text
        self.openapi_model_parser: OpenAPIModelParser = openapi_model_parser or OpenAPIModelParser(
            source=''
        )
        if model_module_name:
            model_module_name_var.set(model_module_name)

    def parse(self) -> ParsedObject:
        openapi = load_yaml(self.input_text)
        return self.parse_paths(openapi)

    def parse_security(
        self, openapi: Dict[str, Any]
    ) -> Optional[List[Dict[str, List[str]]]]:
        return openapi.get('security')

    def parse_info(
        self, openapi: Dict[str, Any]
    ) -> Optional[List[Dict[str, List[str]]]]:
        return openapi.get('info')

    def parse_paths(self, openapi: Dict[str, Any]) -> ParsedObject:
        security = self.parse_security(openapi)
        info = self.parse_info(openapi)
        return ParsedObject(
            [
                operation
                for path_name, operations in openapi['paths'].items()
                for operation in Path(
                    path=UsefulStr(path_name),
                    operations=operations,
                    security=security,
                    components=openapi.get('components', {}),
                    openapi_model_parser=self.openapi_model_parser,
                ).exists_operations
            ],
            info,
        )
