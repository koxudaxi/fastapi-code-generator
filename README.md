# fastapi-code-generator

This code generator creates a FastAPI app from an openapi file.

[![PyPI version](https://badge.fury.io/py/fastapi-code-generator.svg)](https://pypi.python.org/pypi/fastapi-code-generator)
[![Downloads](https://pepy.tech/badge/fastapi-code-generator/month)](https://pepy.tech/project/fastapi-code-generator)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-code-generator)](https://pypi.python.org/pypi/fastapi-code-generator)
[![codecov](https://codecov.io/gh/koxudaxi/fastapi-code-generator/branch/master/graph/badge.svg)](https://codecov.io/gh/koxudaxi/fastapi-code-generator)
![license](https://img.shields.io/github/license/koxudaxi/fastapi-code-generator.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## This project is in experimental phase.

fastapi-code-generator uses [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator) to generate pydantic models

## Help
See [documentation](https://koxudaxi.github.io/fastapi-code-generator) for more details.


## Installation

To install `fastapi-code-generator`:
```sh
$ pip install fastapi-code-generator
```

## Usage

The `fastapi-code-generator` command:
```
Usage: fastapi-codegen [OPTIONS]

Options:
  -i, --input FILENAME     [required]
  -o, --output PATH        [required]
  -t, --template-dir PATH
  -m, --model-file         Specify generated model file path + name, if not default to models.py
  -r, --generate-routers   Generate modular api with multiple routers using RouterAPI (for bigger applications).
  --specify-tags           Use along with --generate-routers to generate specific routers from given list of tags.
  -c, --custom-visitors    PATH - A custom visitor that adds variables to the template.
  --install-completion     Install completion for the current shell.
  --show-completion        Show completion for the current shell, to copy it
                           or customize the installation.
  --help                   Show this message and exit.
```

## Example
### OpenAPI
```sh
$ fastapi-codegen --input api.yaml --output app
```

<details>
<summary>api.yaml</summary>
<pre>
<code>
openapi: "3.0.0"
info:
  version: 1.0.0
  title: Swagger Petstore
  license:
    name: MIT
servers:
  - url: http://petstore.swagger.io/v1
paths:
  /pets:
    get:
      summary: List all pets
      operationId: listPets
      tags:
        - pets
      parameters:
        - name: limit
          in: query
          description: How many items to return at one time (max 100)
          required: false
          schema:
            type: integer
            format: int32
      responses:
        '200':
          description: A paged array of pets
          headers:
            x-next:
              description: A link to the next page of responses
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Pets"
        default:
          description: unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
                x-amazon-apigateway-integration:
                  uri:
                    Fn::Sub: arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${PythonVersionFunction.Arn}/invocations
                  passthroughBehavior: when_no_templates
                  httpMethod: POST
                  type: aws_proxy
    post:
      summary: Create a pet
      operationId: createPets
      tags:
        - pets
      responses:
        '201':
          description: Null response
        default:
          description: unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
                x-amazon-apigateway-integration:
                  uri:
                    Fn::Sub: arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${PythonVersionFunction.Arn}/invocations
                  passthroughBehavior: when_no_templates
                  httpMethod: POST
                  type: aws_proxy
  /pets/{petId}:
    get:
      summary: Info for a specific pet
      operationId: showPetById
      tags:
        - pets
      parameters:
        - name: petId
          in: path
          required: true
          description: The id of the pet to retrieve
          schema:
            type: string
      responses:
        '200':
          description: Expected response to a valid request
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Pets"
        default:
          description: unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
    x-amazon-apigateway-integration:
      uri:
        Fn::Sub: arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${PythonVersionFunction.Arn}/invocations
      passthroughBehavior: when_no_templates
      httpMethod: POST
      type: aws_proxy
components:
  schemas:
    Pet:
      required:
        - id
        - name
      properties:
        id:
          type: integer
          format: int64
        name:
          type: string
        tag:
          type: string
    Pets:
      type: array
      description: list of pet
      items:
        $ref: "#/components/schemas/Pet"
    Error:
      required:
        - code
        - message
      properties:
        code:
          type: integer
          format: int32
        message:
          type: string
</code>
</pre>
</details>


`app/main.py`:
```python
# generated by fastapi-codegen:
#   filename:  api.yaml
#   timestamp: 2020-06-14T10:45:22+00:00

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, Query

from .models import Pets

app = FastAPI(version="1.0.0", title="Swagger Petstore", license="{'name': 'MIT'}",)


@app.get('/pets', response_model=Pets)
def list_pets(limit: Optional[int] = None) -> Pets:
    """
    List all pets
    """
    pass


@app.post('/pets', response_model=None)
def create_pets() -> None:
    """
    Create a pet
    """
    pass


@app.get('/pets/{pet_id}', response_model=Pets)
def show_pet_by_id(pet_id: str = Query(..., alias='petId')) -> Pets:
    """
    Info for a specific pet
    """
    pass

```

`app/models.py`:
```python
# generated by datamodel-codegen:
#   filename:  api.yaml
#   timestamp: 2020-06-14T10:45:22+00:00

from typing import List, Optional

from pydantic import BaseModel, Field


class Pet(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None


class Pets(BaseModel):
    __root__: List[Pet] = Field(..., description='list of pet')


class Error(BaseModel):
    code: int
    message: str
```

## Custom Template
If you want to generate custom `*.py` files then you can give a custom template directory to fastapi-code-generator with `-t` or `--template-dir` options of the command.

fastapi-code-generator will search for [jinja2](https://jinja.palletsprojects.com/) template files in given template directory, for example `some_jinja_templates/list_pets.py`.

```bash
fastapi-code-generator --template-dir some_jinja_templates --output app --input api.yaml
```

These files will be rendered and written to the output directory. Also, the generated file names will be created with the template name and extension of `*.py`, for example `app/list_pets.py` will be a separate file generated from the jinja template alongside the default `app/main.py`

### Variables
You can use the following variables in the jinja2 templates

- `imports`  all imports statements
- `info`  all info statements
- `operations` `operations` is list of `operation`
  - `operation.type` HTTP METHOD
  - `operation.path` Path
  - `operation.snake_case_path` Snake-cased Path
  - `operation.response` response object
  - `operation.function_name` function name is created `operationId` or `METHOD` + `Path` 
  - `operation.snake_case_arguments` Snake-cased function arguments
  - `operation.security` [Security](https://swagger.io/docs/specification/authentication/)
  - `operation.summary` a summary
  - `operation.tags` [Tags](https://swagger.io/docs/specification/grouping-operations-with-tags/)

### default template 
`main.jinja2`
```jinja2
from __future__ import annotations

from fastapi import FastAPI

{{imports}}

app = FastAPI(
    {% if info %}
    {% for key,value in info.items() %}
    {{ key }} = "{{ value }}",
    {% endfor %}
    {% endif %}
    )


{% for operation in operations %}
@app.{{operation.type}}('{{operation.snake_case_path}}', response_model={{operation.response}})
def {{operation.function_name}}({{operation.snake_case_arguments}}) -> {{operation.response}}:
    {%- if operation.summary %}
    """
    {{ operation.summary }}
    """
    {%- endif %}
    pass
{% endfor %}

```

### modular_template
`modular_template/main.jinja2`:
```jinja
from __future__ import annotations

from fastapi import FastAPI

from .routers import {{ routers | join(", ") }}

app = FastAPI(
    {% if info %}
    {% for key,value in info.items() %}
    {% set info_value= value.__repr__() %}
    {{ key }} = {{info_value}},
    {% endfor %}
    {% endif %}
    )

{% for router in routers -%}
app.include_router({{router}}.router)
{% endfor -%}

@app.get("/")
async def root():
    return {"message": "Gateway of the App"}
```

`modular_template/routers.jinja2`:
```jinja
from __future__ import annotations

from fastapi import APIRouter
from fastapi import FastAPI

from ..dependencies import *

router = APIRouter(
    tags=['{{tag}}']
    )

{% for operation in operations %}
{% if operation.tags[0] == tag %}
@router.{{operation.type}}('{{operation.snake_case_path}}', response_model={{operation.response}}
    {% if operation.additional_responses %}
        , responses={
            {% for status_code, models in operation.additional_responses.items() %}
                '{{ status_code }}': {
                {% for key, model in models.items() %}
                    '{{ key }}': {{ model }}{% if not loop.last %},{% endif %}
                {% endfor %}
                }{% if not loop.last %},{% endif %}
            {% endfor %}
        }
    {% endif %}
    {% if operation.tags%}
    , tags={{operation.tags}}
    {% endif %})
def {{operation.function_name}}({{operation.snake_case_arguments}}) -> {{operation.return_type}}:
    {%- if operation.summary %}
    """
    {{ operation.summary }}
    """
    {%- endif %}
    pass
{% endif %}
{% endfor %}
```

`modular_template/dependencies.jinja2`:
```jinja
{{imports}}
```

## Custom Visitors

Custom visitors allow you to pass custom variables to your custom templates.

E.g.

### custom template
`custom-template.jinja2`
```jinja2
#{ % custom_header %}
from __future__ import annotations

from fastapi import FastAPI

...
```

### custom visitor
`custom-visitor.py`
```python
from typing import Dict, Optional

from fastapi_code_generator.parser import OpenAPIParser
from fastapi_code_generator.visitor import Visitor


def custom_visitor(parser: OpenAPIParser, model_path: Path) -> Dict[str, object]:
    return {'custom_header': 'My header'}


visit: Visitor = custom_visitor
```

### Multiple Files using APIRouter (For Bigger Applications)
```
├── app                      # "app" is a Root directory      
│   ├── main.py              # "main" module
│   ├── models.py            # "models" of the application
│   ├── dependencies.py      # "dependencies" module, e.g. import app.dependencies
│   └── routers              # "routers" is a "app subpackage"
│       ├── fat_cats.py      # "fat_cats" submodule, e.g. import app.routers.fat_cats
│       └── slim_dogs.py     # "slim_dogs" submodule, e.g. import app.routers.slim_dogs
```
**_Generate main aside with all of its routers_**:
```bash
$ fastapi-codegen --input swagger.yaml --output app --generate-routers
```

**_Regenerate specific routers_**:
```bash
$ fastapi-codegen --input swagger.yaml --output app --generate-routers --specify-tags "Slim Dogs, Fat Cats"
```


<details>
<summary>swagger.yaml</summary>
<pre>
<code>
openapi: "3.0.0"
info:
  version: 1.0.0
  title: Swagger Petstore
  license:
    name: MIT
servers:
  - url: http://petstore.swagger.io/v1
paths:
  /cats:
    get:
      summary: List All Fat Cats
      operationId: listFatCats
      tags:
        - Fat Cats
      parameters:
        - name: limit
          in: query
          description: How many items to return at one time (max 100)
          required: false
          schema:
            type: integer
      responses:
        '200':
          description: An array of fat cats
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/FatCats"
    post:
      summary: Create a Fat Cat
      operationId: createFatCats
      tags:
        - Fat Cats
      responses:
        '201':
          description: Null response
  /cats/{catId}:
    get:
      summary: Info For a Specific Cat
      operationId: showCatById
      tags:
        - Fat Cats
      parameters:
        - name: catId
          in: path
          required: true
          description: The id of the cat to retrieve
          schema:
            type: string
      responses:
        '200':
          description: Expected response to a valid request
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/FatCats"
  /dogs:
    get:
      summary: List All Slim Dogs
      operationId: listSlimDogs
      tags:
        - Slim Dogs
      parameters:
        - name: limit
          in: query
          description: How many items to return at one time (max 100)
          required: false
          schema:
            type: integer
      responses:
        '200':
          description: An array of slim dogs
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/SlimDogs"
    post:
      summary: Create a Slim Dog
      operationId: createSlimDogs
      tags:
        - Slim Dogs
      responses:
        '201':
          description: Null response
  /dogs/{dogId}:
    get:
      summary: Info For a Specific Dog
      operationId: showDogById
      tags:
        - Slim Dogs
      parameters:
        - name: dogId
          in: path
          required: true
          description: The id of the dog to retrieve
          schema:
            type: string
      responses:
        '200':
          description: Expected response to a valid request
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/SlimDogs"
components:
  schemas:
    Pet:
      required:
        - id
        - name
      properties:
        id:
          type: integer
        name:
          type: string
        tag:
          type: string
    FatCats:
      type: array
      description: list of fat cats
      items:
        $ref: "#/components/schemas/Pet"
    SlimDogs:
      type: array
      description: list of slim dogs
      items:
        $ref: "#/components/schemas/Pet"
</code>
</pre>
</details>

`app/main.py`:

```python
# generated by fastapi-codegen:
#   filename:  swagger.yaml
#   timestamp: 2023-04-04T12:06:16+00:00

from __future__ import annotations

from fastapi import FastAPI

from .routers import fat_cats, slim_dogs

app = FastAPI(
    version='1.0.0',
    title='Swagger Petstore',
    license={'name': 'MIT'},
    servers=[{'url': 'http://petstore.swagger.io/v1'}],
)

app.include_router(fat_cats.router)
app.include_router(slim_dogs.router)


@app.get("/")
async def root():
    return {"message": "Gateway of the App"}
```

`app/models.py`:

```python
# generated by fastapi-codegen:
#   filename:  swagger.yaml
#   timestamp: 2023-04-04T12:06:16+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Pet(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None


class FatCats(BaseModel):
    __root__: List[Pet] = Field(..., description='list of fat cats')


class SlimDogs(BaseModel):
    __root__: List[Pet] = Field(..., description='list of slim dogs')
```

`app/routers/fat_cats.py`:

```python
# generated by fastapi-codegen:
#   filename:  swagger.yaml
#   timestamp: 2023-04-04T12:06:16+00:00

from __future__ import annotations

from fastapi import APIRouter, FastAPI

from ..dependencies import *

router = APIRouter(tags=['Fat Cats'])


@router.get('/cats', response_model=FatCats, tags=['Fat Cats'])
def list_fat_cats(limit: Optional[int] = None) -> FatCats:
    """
    List All Fat Cats
    """
    pass


@router.post('/cats', response_model=None, tags=['Fat Cats'])
def create_fat_cats() -> None:
    """
    Create a Fat Cat
    """
    pass


@router.get('/cats/{cat_id}', response_model=FatCats, tags=['Fat Cats'])
def show_cat_by_id(cat_id: str = Path(..., alias='catId')) -> FatCats:
    """
    Info For a Specific Cat
    """
    pass
```

`app/routers/slim_dogs.py`:

```python
# generated by fastapi-codegen:
#   filename:  swagger.yaml
#   timestamp: 2023-04-04T12:06:16+00:00

from __future__ import annotations

from fastapi import APIRouter, FastAPI

from ..dependencies import *

router = APIRouter(tags=['Slim Dogs'])


@router.get('/dogs', response_model=SlimDogs, tags=['Slim Dogs'])
def list_slim_dogs(limit: Optional[int] = None) -> SlimDogs:
    """
    List All Slim Dogs
    """
    pass


@router.post('/dogs', response_model=None, tags=['Slim Dogs'])
def create_slim_dogs() -> None:
    """
    Create a Slim Dog
    """
    pass


@router.get('/dogs/{dog_id}', response_model=SlimDogs, tags=['Slim Dogs'])
def show_dog_by_id(dog_id: str = Path(..., alias='dogId')) -> SlimDogs:
    """
    Info For a Specific Dog
    """
    pass
```

`app/dependencies.py`:

```python
# generated by fastapi-codegen:
#   filename:  swagger.yaml
#   timestamp: 2023-04-04T12:06:16+00:00

from __future__ import annotations

from typing import Optional

from fastapi import Path

from .models import FatCats, SlimDogs
```
## PyPi 

[https://pypi.org/project/fastapi-code-generator](https://pypi.org/project/fastapi-code-generator)

## License

fastapi-code-generator is released under the MIT License. http://www.opensource.org/licenses/mit-license

