from __future__ import annotations

import pathlib
import re
from functools import cached_property
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
    snooper_to_methods,
)
from datamodel_code_generator.imports import Import, Imports
from datamodel_code_generator.model import DataModel, DataModelFieldBase
from datamodel_code_generator.model import pydantic as pydantic_model
from datamodel_code_generator.model.pydantic import CustomRootType, DataModelField
from datamodel_code_generator.parser.jsonschema import JsonSchemaObject
from datamodel_code_generator.parser.openapi import MediaObject
from datamodel_code_generator.parser.openapi import OpenAPIParser as OpenAPIModelParser
from datamodel_code_generator.parser.openapi import (
    ParameterLocation,
    ParameterObject,
    ReferenceObject,
    RequestBodyObject,
    ResponseObject,
)
from datamodel_code_generator.types import DataType, DataTypeManager, StrictTypes
from pydantic import BaseModel, ValidationInfo

RE_APPLICATION_JSON_PATTERN: Pattern[str] = re.compile(r'^application/.*json$')


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
    def validate(cls, v: Any, info: ValidationInfo) -> Any:
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
    default: Optional[UsefulStr] = None
    default_value: Optional[UsefulStr] = None
    field: Union[DataModelField, list[DataModelField], None] = None
    required: bool

    def __str__(self) -> str:
        return self.argument

    @property
    def argument(self) -> str:
        if self.field is None:
            type_hint = self.type_hint
        else:
            type_hint = (
                UsefulStr(self.field.type_hint)
                if not isinstance(self.field, list)
                else UsefulStr(
                    f"Union[{', '.join(field.type_hint for field in self.field)}]"
                )
            )
        if self.default is None and self.required:
            return f'{self.name}: {type_hint}'
        return f'{self.name}: {type_hint} = {self.default}'

    @property
    def snakecase(self) -> str:
        if self.field is None:
            type_hint = self.type_hint
        else:
            type_hint = (
                UsefulStr(self.field.type_hint)
                if not isinstance(self.field, list)
                else UsefulStr(
                    f"Union[{', '.join(field.type_hint for field in self.field)}]"
                )
            )
        if self.default is None and self.required:
            return f'{stringcase.snakecase(self.name)}: {type_hint}'
        return f'{stringcase.snakecase(self.name)}: {type_hint} = {self.default}'


class Operation(CachedPropertyModel):
    method: UsefulStr
    path: UsefulStr
    operationId: Optional[UsefulStr] = None
    description: Optional[str] = None
    summary: Optional[str] = None
    parameters: List[Dict[str, Any]] = []
    responses: Dict[UsefulStr, Any] = {}
    deprecated: bool = False
    security: Optional[List[Dict[str, List[str]]]] = None
    tags: Optional[List[str]] = []
    request: Optional[Argument] = None
    response: str = ''
    additional_responses: Dict[Union[str, int], Dict[str, str]] = {}
    return_type: str = ''
    callbacks: Dict[UsefulStr, List["Operation"]] = {}
    arguments_list: List[Argument] = []

    @classmethod
    def merge_arguments_with_union(cls, arguments: List[Argument]) -> List[Argument]:
        grouped_arguments: DefaultDict[str, List[Argument]] = DefaultDict(list)
        for argument in arguments:
            grouped_arguments[argument.name].append(argument)

        merged_arguments = []
        for argument_list in grouped_arguments.values():
            if len(argument_list) == 1:
                merged_arguments.append(argument_list[0])
            else:
                argument = argument_list[0]
                fields = [
                    item
                    for arg in argument_list
                    if arg.field is not None
                    for item in (
                        arg.field if isinstance(arg.field, list) else [arg.field]
                    )
                    if item is not None
                ]
                argument.field = fields
                merged_arguments.append(argument)
        return merged_arguments

    @cached_property
    def type(self) -> UsefulStr:
        """
        backwards compatibility
        """
        return self.method

    @property
    def arguments(self) -> str:
        sorted_arguments = Operation.merge_arguments_with_union(self.arguments_list)
        return ", ".join(argument.argument for argument in sorted_arguments)

    @property
    def snake_case_arguments(self) -> str:
        sorted_arguments = Operation.merge_arguments_with_union(self.arguments_list)
        return ", ".join(argument.snakecase for argument in sorted_arguments)

    @property
    def imports(self) -> Imports:
        imports = Imports()
        for argument in self.arguments_list:
            if isinstance(argument.field, list):
                for field in argument.field:
                    imports.append(field.data_type.import_)
            elif argument.field:
                imports.append(argument.field.data_type.import_)
        return imports

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


@snooper_to_methods()
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
        target_python_version: PythonVersion = PythonVersion.PY_39,
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
        self.operations: Dict[str, Operation] = {}
        self._temporary_operation: Dict[str, Any] = {}
        self.imports_for_fastapi: Imports = Imports()
        self.data_types: List[DataType] = []

    def parse_info(self) -> Optional[Dict[str, Any]]:
        result = self.raw_obj.get('info', {}).copy()
        servers = self.raw_obj.get('servers')
        if servers:
            result['servers'] = servers
        return result or None

    def parse_all_parameters(
        self,
        name: str,
        parameters: List[Union[ReferenceObject, ParameterObject]],
        path: List[str],
    ) -> None:
        super().parse_all_parameters(name, parameters, path)
        self._temporary_operation['_parameters'].extend(parameters)

    def get_parameter_type(
        self,
        parameters: Union[ReferenceObject, ParameterObject],
        snake_case: bool,
        path: List[str],
    ) -> Optional[Argument]:
        parameters = self.resolve_object(parameters, ParameterObject)
        if parameters.name is None:
            raise RuntimeError("parameters.name is None")  # pragma: no cover
        orig_name = parameters.name
        name = self.model_resolver.get_valid_field_name(parameters.name)
        if snake_case:
            name = stringcase.snakecase(name)

        schema: Optional[JsonSchemaObject] = None
        data_type: Optional[DataType] = None
        for content in parameters.content.values():
            if isinstance(content.schema_, ReferenceObject):
                data_type = self.get_ref_data_type(content.schema_.ref)
                ref_model = self.get_ref_model(content.schema_.ref)
                schema = JsonSchemaObject.parse_obj(ref_model)
            else:
                schema = content.schema_
            break
        if not data_type:
            if not schema:
                schema = parameters.schema_
            if schema is None:
                raise RuntimeError("schema is None")  # pragma: no cover
            data_type = self.parse_schema(name, schema, [*path, name])
            data_type = self._collapse_root_model(data_type)
        if not schema:
            return None

        field = DataModelField(
            name=name,
            data_type=data_type,
            required=parameters.required or parameters.in_ == ParameterLocation.path,
        )

        if orig_name != name:
            if parameters.in_:
                param_is = parameters.in_.value.lower().capitalize()
                self.imports_for_fastapi.append(
                    Import(from_='fastapi', import_=param_is)
                )
                default: Optional[str] = (
                    f"{param_is}({'...' if field.required else repr(schema.default)}, alias='{orig_name}')"
                )
        else:
            default = repr(schema.default) if schema.has_default else None
        self.imports_for_fastapi.append(field.imports)
        self.data_types.append(field.data_type)
        return Argument(
            name=UsefulStr(field.name),
            type_hint=UsefulStr(field.type_hint),
            default=default,  # type: ignore
            default_value=schema.default,
            required=field.required,
            field=field,
        )

    def get_arguments(self, snake_case: bool, path: List[str]) -> str:
        return ", ".join(
            argument.argument for argument in self.get_argument_list(snake_case, path)
        )

    def get_argument_list(self, snake_case: bool, path: List[str]) -> List[Argument]:
        arguments: List[Argument] = []

        parameters = self._temporary_operation.get('_parameters')
        if parameters:
            for parameter in parameters:
                parameter_type = self.get_parameter_type(
                    parameter, snake_case, [*path, 'parameters']
                )
                if parameter_type:
                    arguments.append(parameter_type)

        request = self._temporary_operation.get('_request')
        if request:
            arguments.append(request)

        positional_argument: bool = False
        for argument in arguments:
            if positional_argument and argument.required and argument.default is None:
                argument.default = UsefulStr('...')
            positional_argument = (
                argument.required
                or (argument.default is not None)
                or argument.type_hint.startswith('Optional[')
            )

        # check if there are duplicate argument.name
        argument_names = [argument.name for argument in arguments]
        if len(argument_names) != len(set(argument_names)):
            self.imports_for_fastapi.append(Import(from_='typing', import_="Union"))
        return arguments

    def parse_request_body(
        self,
        name: str,
        request_body: RequestBodyObject,
        path: List[str],
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
                    data_type = self._collapse_root_model(data_type)
                    arguments.append(
                        # TODO: support multiple body
                        Argument(
                            name='body',  # type: ignore
                            type_hint=UsefulStr(data_type.type_hint),
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
                elif media_type == 'application/octet-stream':
                    arguments.append(
                        Argument(
                            name='request',  # type: ignore
                            type_hint='Request',  # type: ignore
                            required=True,
                        )
                    )
                    self.imports_for_fastapi.append(
                        Import.from_full_path("fastapi.Request")
                    )
                elif media_type == 'multipart/form-data':
                    arguments.append(
                        Argument(
                            name='file',  # type: ignore
                            type_hint='UploadFile',  # type: ignore
                            required=True,
                        )
                    )
                    self.imports_for_fastapi.append(
                        Import.from_full_path("fastapi.UploadFile")
                    )
        self._temporary_operation['_request'] = arguments[0] if arguments else None

    def parse_responses(  # type: ignore[override]
        self,
        name: str,
        responses: Dict[str, Union[ResponseObject, ReferenceObject]],
        path: List[str],
    ) -> Dict[Union[str, int], Dict[str, DataType]]:
        data_types = super().parse_responses(name, responses, path)  # type: ignore[arg-type]
        status_code_200 = data_types.get('200')
        if status_code_200:
            data_type = list(status_code_200.values())[0]
            if data_type:
                data_type = self._collapse_root_model(data_type)
                self.data_types.append(data_type)
        else:
            data_type = DataType(type='None')
        type_hint = data_type.type_hint  # TODO: change to lazy loading
        self._temporary_operation['response'] = type_hint
        return_types = {type_hint: data_type}
        for status_code, additional_responses in data_types.items():
            if status_code != '200' and additional_responses:  # 200 is processed above
                data_type = list(additional_responses.values())[0]
                if data_type:
                    self.data_types.append(data_type)
                type_hint = data_type.type_hint  # TODO: change to lazy loading
                self._temporary_operation.setdefault('additional_responses', {})[
                    status_code
                ] = {'model': type_hint}
                return_types[type_hint] = data_type
        if len(return_types) == 1:
            return_type = next(iter(return_types.values()))
        else:
            return_type = DataType(data_types=list(return_types.values()))
        if return_type:
            self.data_types.append(return_type)
        self._temporary_operation['return_type'] = return_type.type_hint
        return data_types

    def parse_operation(
        self,
        raw_operation: Dict[str, Any],
        path: List[str],
    ) -> None:
        self._temporary_operation = {}
        self._temporary_operation['_parameters'] = []
        super().parse_operation(raw_operation, path)
        resolved_path = self.model_resolver.resolve_ref(path)
        path_name, method = path[-2:]

        self._temporary_operation['arguments_list'] = self.get_argument_list(
            snake_case=True, path=path
        )
        main_operation = self._temporary_operation

        # Handle callbacks. This iterates over callbacks, shifting each one
        # into the `_temporary_operation` and parsing it. Parsing could be
        # refactored into a recursive operation to simplify this routine.
        cb_ctr = 0
        callbacks: Dict[UsefulStr, list[Operation]] = {}
        if 'callbacks' in raw_operation:
            raw_callbacks = raw_operation.pop('callbacks')
            for key, routes in raw_callbacks.items():
                if key not in callbacks:
                    callbacks[key] = []
                for route, methods in routes.items():
                    for method, cb_op in methods.items():
                        # Since the path is often generated dynamically from
                        # the contents of the original request (such as by
                        # passing a `callbackUrl`), it won't work to generate
                        # a function name from the path. Instead, inject a
                        # placeholder `operationId` in order to get a unique
                        # and reasonable function name for the operation.
                        if 'operationId' not in cb_op:
                            cb_op['operationId'] = f"{method}_{key}_{cb_ctr}"
                            cb_ctr += 1

                        self._temporary_operation = {'_parameters': []}
                        cb_path = path + ['callbacks', key, route, method]
                        super().parse_operation(cb_op, cb_path)
                        self._temporary_operation['arguments_list'] = (
                            self.get_argument_list(snake_case=True, path=cb_path)
                        )

                        callbacks[key].append(
                            Operation(
                                **cb_op,
                                **self._temporary_operation,
                                path=route,
                                method=method,  # type: ignore
                            )
                        )

        self.operations[resolved_path] = Operation(
            **raw_operation,
            **main_operation,
            callbacks=callbacks,
            path=f'/{path_name}',  # type: ignore
            method=method,  # type: ignore
        )

    def _collapse_root_model(self, data_type: DataType) -> DataType:
        reference = data_type.reference
        import functools

        try:
            if not (
                reference
                and (
                    len(reference.children) == 0
                    or functools.reduce(lambda a, b: a == b, reference.children)
                )
            ):
                return data_type
        except RecursionError:
            return data_type
        source = reference.source
        if not isinstance(source, CustomRootType):
            return data_type
        data_type.remove_reference()
        data_type = source.fields[0].data_type
        if source in self.results:
            self.results.remove(source)
        return data_type
