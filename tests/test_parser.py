from pathlib import Path

import pytest
from datamodel_code_generator.parser.jsonschema import JsonSchemaObject
from datamodel_code_generator.parser.openapi import ReferenceObject, RequestBodyObject

from fastapi_code_generator.parser import OpenAPIParser, UsefulStr, snakecase


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("listPets", "list_pets"),
        ("pet-id", "pet_id"),
        ("pet.id", "pet_id"),
        ("pet id", "pet_id"),
        ("{petId}", "{pet_id}"),
        ("HTTPStatus", "h_t_t_p_status"),
        ("", ""),
    ],
)
def test_snakecase_matches_legacy_stringcase_behavior(
    value: str, expected: str
) -> None:
    assert snakecase(value) == expected


@pytest.mark.parametrize(
    ("value", "expected_snake", "expected_camel", "expected_pascal"),
    [
        ("sample_name", "sample_name", "sampleName", "SampleName"),
        ("listPets", "list_pets", "listPets", "ListPets"),
        ("SampleName", "sample_name", "sampleName", "SampleName"),
        ("", "", "", ""),
    ],
)
def test_useful_str_case_helpers_match_legacy_stringcase_behavior(
    value: str, expected_snake: str, expected_camel: str, expected_pascal: str
) -> None:
    useful_value = UsefulStr(value)

    assert useful_value.snakecase == expected_snake
    assert useful_value.camelcase == expected_camel
    assert useful_value.pascalcase == expected_pascal


def assert_field_extras(
    parser: OpenAPIParser, schema_data: dict[str, object], expected: dict[str, object]
) -> None:
    schema = JsonSchemaObject.model_validate(schema_data)
    assert parser.get_field_extras(schema) == expected


def test_get_upload_file_type_resolves_reference(tmp_path: Path) -> None:
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(
        """
openapi: 3.0.0
info:
  title: Test
  version: '1.0'
paths: {}
components:
  schemas:
    Uploads:
      type: object
      properties:
        images:
          type: array
          items:
            type: string
            format: binary
""",
        encoding="utf-8",
    )
    parser = OpenAPIParser(schema_path)
    parser.parse_raw()

    file_name, type_hint = parser._get_upload_file_type(
        ReferenceObject.model_validate({"$ref": "#/components/schemas/Uploads"})
    )

    assert file_name == "images"
    assert type_hint == "List[UploadFile]"
    assert parser.imports_for_fastapi["typing"] == {"List"}


@pytest.mark.parametrize("value", [True, None, "string", 123, {}, []])
def test_is_upload_file_array_rejects_non_schema(value: object) -> None:
    parser = OpenAPIParser(
        "openapi: 3.0.0\ninfo: {title: Test, version: '1.0'}\npaths: {}\n"
    )

    assert parser._is_upload_file_array(value) is False


def test_get_upload_file_name_falls_back_when_properties_are_not_uploads() -> None:
    parser = OpenAPIParser(
        "openapi: 3.0.0\ninfo: {title: Test, version: '1.0'}\npaths: {}\n"
    )
    schema = JsonSchemaObject.model_validate(
        {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                }
            },
        }
    )

    assert parser._get_upload_file_name(schema) == "file"


def test_get_upload_file_type_uses_single_binary_property_name() -> None:
    parser = OpenAPIParser(
        "openapi: 3.0.0\ninfo: {title: Test, version: '1.0'}\npaths: {}\n"
    )
    schema = JsonSchemaObject.model_validate(
        {
            "type": "object",
            "properties": {
                "avatar": {
                    "type": "string",
                    "format": "binary",
                }
            },
        }
    )

    assert parser._get_upload_file_type(schema) == ("avatar", "UploadFile")


def test_parse_request_body_filters_multipart_from_mixed_content() -> None:
    parser = OpenAPIParser(
        "openapi: 3.0.0\ninfo: {title: Test, version: '1.0'}\npaths: {}\n"
    )
    request_body = RequestBodyObject.model_validate(
        {
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "file": {
                                "type": "string",
                                "format": "binary",
                            }
                        },
                    }
                },
                "application/json": {
                    "schema": {
                        "type": "string",
                    }
                },
            }
        }
    )

    request_body_fields = parser.parse_request_body(
        "MixedUpload", request_body, ["paths", "mixed", "post", "requestBody"]
    )

    assert set(request_body_fields) == {"application/json"}


def test_get_field_extras_preserves_non_union_discriminator() -> None:
    parser = OpenAPIParser(
        "openapi: 3.0.0\ninfo: {title: Test, version: '1.0'}\npaths: {}\n"
    )
    assert_field_extras(
        parser,
        {
            "type": "object",
            "discriminator": {
                "propertyName": "kind",
            },
        },
        {"discriminator": {"propertyName": "kind"}},
    )


def test_get_field_extras_removes_discriminator_for_all_of_simple_variant() -> None:
    parser = OpenAPIParser(
        "openapi: 3.0.0\ninfo: {title: Test, version: '1.0'}\npaths: {}\n"
    )
    assert_field_extras(
        parser,
        {
            "oneOf": [
                {
                    "allOf": [
                        {
                            "type": "string",
                        }
                    ]
                },
                {
                    "type": "object",
                    "properties": {
                        "kind": {
                            "type": "string",
                        },
                    },
                },
            ],
            "discriminator": {
                "propertyName": "kind",
            },
        },
        {},
    )


def test_get_field_extras_preserves_discriminator_for_all_of_object_variant() -> None:
    parser = OpenAPIParser(
        "openapi: 3.0.0\ninfo: {title: Test, version: '1.0'}\npaths: {}\n"
    )
    assert_field_extras(
        parser,
        {
            "oneOf": [
                {
                    "allOf": [
                        {
                            "type": "object",
                            "properties": {
                                "kind": {
                                    "type": "string",
                                },
                            },
                        }
                    ]
                },
                {
                    "type": "object",
                    "properties": {
                        "kind": {
                            "type": "string",
                        },
                    },
                },
            ],
            "discriminator": {
                "propertyName": "kind",
            },
        },
        {"discriminator": {"propertyName": "kind"}},
    )


def test_get_field_extras_removes_discriminator_for_cyclic_all_of_ref(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    parser = OpenAPIParser(
        "openapi: 3.0.0\ninfo: {title: Test, version: '1.0'}\npaths: {}\n"
    )
    schema_ref = "#/components/schemas/Loop"

    def get_ref_model(ref: str) -> dict[str, object]:
        return {"allOf": [{"$ref": ref}]}

    monkeypatch.setattr(parser, "get_ref_model", get_ref_model)
    assert_field_extras(
        parser,
        {
            "oneOf": [
                {
                    "$ref": schema_ref,
                },
                {
                    "type": "object",
                    "properties": {
                        "kind": {
                            "type": "string",
                        },
                    },
                },
            ],
            "discriminator": {
                "propertyName": "kind",
            },
        },
        {},
    )


def test_get_field_extras_checks_one_of_and_any_of_variants() -> None:
    parser = OpenAPIParser(
        "openapi: 3.0.0\ninfo: {title: Test, version: '1.0'}\npaths: {}\n"
    )
    assert_field_extras(
        parser,
        {
            "oneOf": [
                {
                    "type": "object",
                    "properties": {
                        "kind": {
                            "type": "string",
                        },
                    },
                },
            ],
            "anyOf": [
                {
                    "type": "string",
                },
            ],
            "discriminator": {
                "propertyName": "kind",
            },
        },
        {},
    )
