from pathlib import Path

import pytest
from datamodel_code_generator.parser.jsonschema import JsonSchemaObject
from datamodel_code_generator.parser.openapi import ReferenceObject, RequestBodyObject

from fastapi_code_generator.parser import OpenAPIParser


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
