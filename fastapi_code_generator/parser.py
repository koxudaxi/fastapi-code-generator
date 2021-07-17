from __future__ import annotations

import pathlib
import re
from contextvars import ContextVar
from typing import (
    Any,
    Callable,
    DefaultDict,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Pattern,
    Sequence,
    Set,
    Type,
    Union,
)
from urllib.parse import ParseResult

import stringcase
from datamodel_code_generator import (
    DefaultPutDict,
    LiteralType,
    OpenAPIScope,
    PythonVersion,
    cached_property,
    snooper_to_methods,
)
from datamodel_code_generator.imports import Import, Imports
from datamodel_code_generator.model import DataModel, DataModelFieldBase
from datamodel_code_generator.model import pydantic as pydantic_model
from datamodel_code_generator.model.pydantic import DataModelField
from datamodel_code_generator.parser.jsonschema import (
    JsonSchemaObject,
    get_model_by_path,
)
from datamodel_code_generator.parser.openapi import MediaObject
from datamodel_code_generator.parser.openapi import OpenAPIParser as OpenAPIModelParser
from datamodel_code_generator.parser.openapi import (
    ParameterObject,
    ReferenceObject,
    RequestBodyObject,
    ResponseObject,
)
from datamodel_code_generator.types import DataType, DataTypeManager, StrictTypes
from pydantic import BaseModel

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
    method: UsefulStr
    path: UsefulStr
    operationId: Optional[UsefulStr]
    summary: Optional[str]
    parameters: List[Dict[str, Any]] = []
    responses: Dict[UsefulStr, Any] = {}
    # requestBody: Dict[str, Any] = {}
    imports: List[Import] = []
    security: Optional[List[Dict[str, List[str]]]] = None
    # components: Dict[str, Any] = {}
    tags: Optional[List[str]]
    arguments: str = ''
    snake_case_arguments: str = ''
    request: Optional[Argument] = None
    response: str = ''

    @cached_property
    def type(self) -> UsefulStr:
        """
        backwards compatibility
        """
        return self.method

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
    def function_name(self) -> str:
        if self.operationId:
            name: str = self.operationId
        else:
            path = re.sub(r'/{|/', '_', self.snake_case_path).replace('}', '')
            name = f"{self.type}{path}"
        return stringcase.snakecase(name)


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
            self.imports.append(operation.imports)


@snooper_to_methods(max_variable_length=None)
class OpenAPIParser(OpenAPIModelParser):
    def __init__(
        self,
        source: Union[str, pathlib.Path, List[pathlib.Path], ParseResult],
        *,
        data_model_type: Type[DataModel] = pydantic_model.BaseModel,
        data_model_root_type: Type[DataModel] = pydantic_model.CustomRootType,
        data_type_manager_type: Type[DataTypeManager] = pydantic_model.DataTypeManager,
        data_model_field_type: Type[DataModelFieldBase] = pydantic_model.DataModelField,
        base_class: Optional[str] = None,
        custom_template_dir: Optional[pathlib.Path] = None,
        extra_template_data: Optional[DefaultDict[str, Dict[str, Any]]] = None,
        target_python_version: PythonVersion = PythonVersion.PY_37,
        dump_resolve_reference_action: Optional[Callable[[Iterable[str]], str]] = None,
        validation: bool = False,
        field_constraints: bool = False,
        snake_case_field: bool = False,
        strip_default_none: bool = False,
        aliases: Optional[Mapping[str, str]] = None,
        allow_population_by_field_name: bool = False,
        apply_default_values_for_required_fields: bool = False,
        force_optional_for_required_fields: bool = False,
        class_name: Optional[str] = None,
        use_standard_collections: bool = False,
        base_path: Optional[pathlib.Path] = None,
        use_schema_description: bool = False,
        reuse_model: bool = False,
        encoding: str = 'utf-8',
        enum_field_as_literal: Optional[LiteralType] = None,
        set_default_enum_member: bool = False,
        strict_nullable: bool = False,
        use_generic_container_types: bool = False,
        enable_faux_immutability: bool = False,
        remote_text_cache: Optional[DefaultPutDict[str, str]] = None,
        disable_appending_item_suffix: bool = False,
        strict_types: Optional[Sequence[StrictTypes]] = None,
        empty_enum_field_name: Optional[str] = None,
        custom_class_name_generator: Optional[Callable[[str], str]] = None,
        field_extra_keys: Optional[Set[str]] = None,
        field_include_all_keys: bool = False,
        model_module_name: Optional[str] = None,
    ):
        super().__init__(
            source=source,
            data_model_type=data_model_type,
            data_model_root_type=data_model_root_type,
            data_type_manager_type=data_type_manager_type,
            data_model_field_type=data_model_field_type,
            base_class=base_class,
            custom_template_dir=custom_template_dir,
            extra_template_data=extra_template_data,
            target_python_version=target_python_version,
            dump_resolve_reference_action=dump_resolve_reference_action,
            validation=validation,
            field_constraints=field_constraints,
            snake_case_field=snake_case_field,
            strip_default_none=strip_default_none,
            aliases=aliases,
            allow_population_by_field_name=allow_population_by_field_name,
            apply_default_values_for_required_fields=apply_default_values_for_required_fields,
            force_optional_for_required_fields=force_optional_for_required_fields,
            class_name=class_name,
            use_standard_collections=use_standard_collections,
            base_path=base_path,
            use_schema_description=use_schema_description,
            reuse_model=reuse_model,
            encoding=encoding,
            enum_field_as_literal=enum_field_as_literal,
            set_default_enum_member=set_default_enum_member,
            strict_nullable=strict_nullable,
            use_generic_container_types=use_generic_container_types,
            enable_faux_immutability=enable_faux_immutability,
            remote_text_cache=remote_text_cache,
            disable_appending_item_suffix=disable_appending_item_suffix,
            strict_types=strict_types,
            empty_enum_field_name=empty_enum_field_name,
            custom_class_name_generator=custom_class_name_generator,
            field_extra_keys=field_extra_keys,
            field_include_all_keys=field_include_all_keys,
            openapi_scopes=[OpenAPIScope.Schemas, OpenAPIScope.Paths],
        )
        if model_module_name:
            model_module_name_var.set(model_module_name)
        self.operations: Dict[str, Operation] = {}
        self._temporary_operation_items: Dict[str, Any] = {}
        self.imports_for_fastapi: Imports = Imports()
        self.data_types: List[DataType] = []

    def parse_info(
        self, openapi: Dict[str, Any]
    ) -> Optional[List[Dict[str, List[str]]]]:
        return openapi.get('info')

    def parse_parameters(self, parameters: ParameterObject, path: List[str]) -> None:
        super().parse_parameters(parameters, path)

    def get_parameter_type(
        self,
        parameter: Dict[str, Union[str, Dict[str, Any]]],
        snake_case: bool,
        path: List[str],
    ) -> Argument:
        ref: Optional[str] = parameter.get('$ref')  # type: ignore
        if ref:
            parameter = self.get_ref_model(ref)
        name: str = parameter["name"]  # type: ignore
        orig_name = name
        if snake_case:
            name = stringcase.snakecase(name)
        content = parameter.get('content')
        schema: Optional[JsonSchemaObject] = None
        if content and isinstance(content, dict):
            content_schema = [
                c.get("schema")
                for c in content.values()
                if isinstance(c.get("schema"), dict)
            ]
            if content_schema:
                schema = JsonSchemaObject.parse_obj(content_schema[0])
        if not schema:
            schema = JsonSchemaObject.parse_obj(parameter["schema"])

        field = DataModelField(
            name=name,
            data_type=self.parse_schema(name, schema, [*path, name]),
            required=parameter.get("required") or parameter.get("in") == "path",
        )

        if orig_name != name:
            has_in = parameter.get('in')
            if has_in and isinstance(has_in, str):
                param_is = has_in.lower().capitalize()
                self.imports_for_fastapi.append(
                    Import(from_='fastapi', import_=param_is)
                )
                default: Optional[
                    str
                ] = f"{param_is}({'...' if field.required else repr(schema.default)}, alias='{orig_name}')"
            else:
                # https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#parameterObject
                # the spec says 'in' is a str type
                raise TypeError(
                    f'Issue processing parameter for "in", expected a str, but got something else: {str(parameter)}'
                )
        else:
            default = repr(schema.default) if schema.has_default else None
        self.imports_for_fastapi.append(field.imports)
        self.data_types.append(field.data_type)
        return Argument(
            name=field.name,
            type_hint=field.type_hint,
            default=default,  # type: ignore
            default_value=schema.default,
            required=field.required,
        )

    def get_arguments(self, snake_case: bool, path: List[str]) -> str:
        return ", ".join(
            argument.argument for argument in self.get_argument_list(snake_case, path)
        )

    def get_argument_list(self, snake_case: bool, path: List[str]) -> List[Argument]:
        arguments: List[Argument] = []

        parameters = self._temporary_operation_items.get('_parameters')
        if parameters:
            for parameter in parameters:
                arguments.append(
                    self.get_parameter_type(
                        parameter, snake_case, [*path, 'parameters']
                    )
                )

        request = self._temporary_operation_items.get('_request')
        if request:
            arguments.append(request)

        if self.request:
            arguments.append(self.request)

        positional_argument: bool = False
        for argument in arguments:
            if positional_argument and argument.required and argument.default is None:
                argument.default = UsefulStr('...')
            positional_argument = argument.required

        return arguments

    def parse_request_body(
        self, name: str, request_body: RequestBodyObject, path: List[str],
    ) -> None:
        super().parse_request_body(name, request_body, path)
        arguments: List[Argument] = []
        for (
            media_type,
            media_obj,
        ) in request_body.content.items():  # type: str, MediaObject
            if isinstance(
                media_obj.schema_, (JsonSchemaObject, ReferenceObject)
            ):  # pragma: no cover
                # TODO: support other content-types
                if RE_APPLICATION_JSON_PATTERN.match(media_type):
                    if isinstance(media_obj.schema_, ReferenceObject):
                        data_type = self.get_ref_data_type(media_obj.schema_.ref)
                    else:
                        data_type = self.parse_schema(
                            name, media_obj.schema_, [*path, media_type]
                        )
                    arguments.append(
                        # TODO: support multiple body
                        Argument(
                            name='body',  # type: ignore
                            type_hint=data_type.type_hint,
                            required=request_body.required,
                        )
                    )
                    self.data_types.append(data_type)
                elif media_type == 'application/x-www-form-urlencoded':
                    arguments.append(
                        # TODO: support form with `Form()`
                        Argument(
                            name='request',  # type: ignore
                            type_hint='Request',  # type: ignore
                            required=True,
                        )
                    )
                    self.imports_for_fastapi.append(
                        Import.from_full_path('starlette.requests.Request')
                    )
        self._temporary_operation_items['_request'] = (
            arguments[0] if arguments else None
        )

    def parse_responses(
        self,
        name: str,
        responses: Dict[str, Union[ResponseObject, ReferenceObject]],
        path: List[str],
    ) -> Dict[str, Dict[str, DataType]]:
        data_types = super().parse_responses(name, responses, path)
        status_code_200 = data_types.get('200')
        if status_code_200:
            data_type = list(status_code_200.values())[0]
            if data_type:
                self.data_types.append(data_type)
            type_hint = data_type.type_hint  # TODO: change to lazy loading
        else:
            type_hint = 'None'
        self._temporary_operation_items['response'] = type_hint

        return data_types

    def parse_operation(self, raw_operation: Dict[str, Any], path: List[str],) -> None:
        self._temporary_operation_items = {}
        super().parse_operation(raw_operation, path)
        resolved_path = self.model_resolver.resolve_ref(path)
        path_name, method = path[-2:]

        self._temporary_operation_items['_parameters'] = raw_operation.get('parameters')
        self._temporary_operation_items['arguments'] = self.get_arguments(
            snake_case=False, path=path
        )
        self._temporary_operation_items['snake_case_arguments'] = self.get_arguments(
            snake_case=True, path=path
        )

        self.operations[resolved_path] = Operation(
            **raw_operation,
            **self._temporary_operation_items,
            path=f'/{path_name}',  # type: ignore
            method=method,  # type: ignore
        )

    def parse_paths(self) -> ParsedObject:
        info = self.parse_info(self.raw_obj)
        return ParsedObject(list(self.operations.values()), info,)
