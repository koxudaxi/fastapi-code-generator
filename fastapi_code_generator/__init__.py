# Copyright (c) 2023 - 2025, AG2ai, Inc., AG2ai open-source projects maintainers and core contributors
#
# SPDX-License-Identifier: Apache-2.0
import logging
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)

from datamodel_code_generator.parser import base
from datamodel_code_generator.model.base import DataModel

# Save the original method before patching
original_parse = base.Parser.parse

def patch_parse() -> None:  # noqa: C901
    def __alias_shadowed_imports(
        self,
        models: list[DataModel],
        all_model_field_names: set[str],
    ) -> None:
        for model in models:
            for model_field in model.fields:
                if model_field.data_type.type in all_model_field_names:
                    alias = model_field.data_type.type + "_aliased"
                    model_field.data_type.type = alias
                    model_field.data_type.import_.alias = alias

    def _parse(  # noqa: PLR0912, PLR0914, PLR0915
        self,
        with_import: bool | None = True,  # noqa: FBT001, FBT002
        format_: bool | None = True,  # noqa: FBT001, FBT002
        settings_path: Path | None = None,
    ) -> str | dict[tuple[str, ...], base.Result]:
        self.parse_raw()

        if with_import:
            self.imports.append(base.IMPORT_ANNOTATIONS)

        if format_:
            code_formatter: base.CodeFormatter | None = base.CodeFormatter(
                self.target_python_version,
                settings_path,
                self.wrap_string_literal,
                skip_string_normalization=not self.use_double_quotes,
                known_third_party=self.known_third_party,
                custom_formatters=self.custom_formatter,
                custom_formatters_kwargs=self.custom_formatters_kwargs,
                encoding=self.encoding,
                formatters=self.formatters,
            )
        else:
            code_formatter = None

        _, sorted_data_models, require_update_action_models = base.sort_data_models(self.results)

        results: dict[tuple[str, ...], base.Result] = {}

        def module_key(data_model: DataModel) -> tuple[str, ...]:
            return tuple(data_model.module_path)

        def sort_key(data_model: DataModel) -> tuple[int, tuple[str, ...]]:
            return (len(data_model.module_path), tuple(data_model.module_path))

        # process in reverse order to correctly establish module levels
        grouped_models = base.groupby(
            sorted(sorted_data_models.values(), key=sort_key, reverse=True),
            key=module_key,
        )

        module_models: list[tuple[tuple[str, ...], list[DataModel]]] = []
        unused_models: list[DataModel] = []
        model_to_module_models: dict[DataModel, tuple[tuple[str, ...], list[DataModel]]] = {}
        module_to_import: dict[tuple[str, ...], base.Imports] = {}

        previous_module: tuple[str, ...] = ()
        for module, models in ((k, [*v]) for k, v in grouped_models):
            for model in models:
                model_to_module_models[model] = module, models
            self._Parser__delete_duplicate_models(models)
            self._Parser__replace_duplicate_name_in_module(models)
            if len(previous_module) - len(module) > 1:
                module_models.extend(
                    (
                        previous_module[:parts],
                        [],
                    )
                    for parts in range(len(previous_module) - 1, len(module), -1)
                )
            module_models.append((
                module,
                models,
            ))
            previous_module = module

        class Processed(base.NamedTuple):
            module: tuple[str, ...]
            models: list[DataModel]
            init: bool
            imports: base.Imports
            scoped_model_resolver: base.ModelResolver

        processed_models: list[Processed] = []

        for module_, models in module_models:
            imports = module_to_import[module_] = base.Imports(self.use_exact_imports)
            init = False
            if module_:
                parent = (*module_[:-1], "__init__.py")
                if parent not in results:
                    results[parent] = base.Result(body="")
                if (*module_, "__init__.py") in results:
                    module = (*module_, "__init__.py")
                    init = True
                else:
                    module = tuple(part.replace("-", "_") for part in (*module_[:-1], f"{module_[-1]}.py"))
            else:
                module = ("__init__.py",)

            all_module_fields = {field.name for model in models for field in model.fields if field.name is not None}
            scoped_model_resolver = base.ModelResolver(exclude_names=all_module_fields)

            self.__alias_shadowed_imports(models, all_module_fields)
            self._Parser__override_required_field(models)
            self._Parser__replace_unique_list_to_set(models)
            self._Parser__change_from_import(models, imports, scoped_model_resolver, init)
            self._Parser__extract_inherited_enum(models)
            self._Parser__set_reference_default_value_to_field(models)
            self._Parser__reuse_model(models, require_update_action_models)
            self._Parser__collapse_root_models(models, unused_models, imports, scoped_model_resolver)
            self._Parser__set_default_enum_member(models)
            self._Parser__sort_models(models, imports)
            self._Parser__change_field_name(models)
            self._Parser__apply_discriminator_type(models, imports)
            self._Parser__set_one_literal_on_default(models)

            processed_models.append(Processed(module, models, init, imports, scoped_model_resolver))

        for processed_model in processed_models:
            for model in processed_model.models:
                processed_model.imports.append(model.imports)

        for unused_model in unused_models:
            module, models = model_to_module_models[unused_model]
            if unused_model in models:  # pragma: no cover
                imports = module_to_import[module]
                imports.remove(unused_model.imports)
                models.remove(unused_model)

        for processed_model in processed_models:
            # postprocess imports to remove unused imports.
            model_code = str("\n".join([str(m) for m in processed_model.models]))
            unused_imports = [
                (from_, import_)
                for from_, imports_ in processed_model.imports.items()
                for import_ in imports_
                if import_ not in model_code
            ]
            for from_, import_ in unused_imports:
                processed_model.imports.remove(Import(from_=from_, import_=import_))

        for module, models, init, imports, scoped_model_resolver in processed_models:  # noqa: B007
            # process after removing unused models
            self._Parser__change_imported_model_name(models, imports, scoped_model_resolver)

        for module, models, init, imports, scoped_model_resolver in processed_models:  # noqa: B007
            result: list[str] = []
            if models:
                if with_import:
                    result += [str(self.imports), str(imports), "\n"]

                code = base.dump_templates(models)
                result += [code]

                if self.dump_resolve_reference_action is not None:
                    result += [
                        "\n",
                        self.dump_resolve_reference_action(
                            m.reference.short_name for m in models if m.path in require_update_action_models
                        ),
                    ]
            if not result and not init:
                continue
            body = "\n".join(result)
            if code_formatter:
                body = code_formatter.format_code(body)

            results[module] = base.Result(body=body, source=models[0].file_path if models else None)

        # retain existing behaviour
        if [*results] == [("__init__.py",)]:
            return results["__init__.py",].body

        results = {tuple(i.replace("-", "_") for i in k): v for k, v in results.items()}
        return (
            self._Parser__postprocess_result_modules(results)
            if self.treat_dot_as_module
            else {
                tuple((part[: part.rfind(".")].replace(".", "_") + part[part.rfind(".") :]) for part in k): v
                for k, v in results.items()
            }
        )


    base.Parser.parse = _parse
    base.Parser.__alias_shadowed_imports = __alias_shadowed_imports

    logger.info("Patched Parser.parse method.")

patch_parse()


