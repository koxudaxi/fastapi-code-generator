from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi_code_generator.__main__ import generate_code


def test_path_parameter_referenced_string_schema_reused_in_body_stays_primitive():
    spec = """\
openapi: 3.0.0
info:
  title: Widget API
  version: 1.0.0
paths:
  /widgets/{widgetId}:
    get:
      operationId: getWidget
      parameters:
        - $ref: '#/components/parameters/WidgetIdParameter'
      responses:
        '200':
          description: ok
  /widgets:
    post:
      operationId: createWidget
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateWidgetBody'
      responses:
        '201':
          description: created
components:
  parameters:
    WidgetIdParameter:
      name: widgetId
      in: path
      required: true
      schema:
        $ref: '#/components/schemas/WidgetId'
  schemas:
    WidgetId:
      type: string
      pattern: '^[A-Z0-9_]+$'
    CreateWidgetBody:
      type: object
      required:
        - widgetId
        - name
      properties:
        widgetId:
          $ref: '#/components/schemas/WidgetId'
        name:
          type: string
"""

    with TemporaryDirectory() as tmp_dir:
        output_dir = Path(tmp_dir)
        generate_code(
            input_name='reused_widget_id.yaml',
            input_text=spec,
            encoding='utf-8',
            output_dir=output_dir,
            template_dir=None,
        )

        main_py = (output_dir / 'main.py').read_text()

    assert "widget_id: WidgetId = Path(..., alias='widgetId')" not in main_py
    assert (
        "widget_id: constr(regex=r'^[A-Z0-9_]+$') = Path(..., alias='widgetId')"
        in main_py
    )
