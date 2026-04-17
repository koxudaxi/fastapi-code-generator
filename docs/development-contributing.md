# Development

Install the package in editable mode:

```sh
$ git clone git@github.com:koxudaxi/fastapi-code-generator.git
$ cd fastapi-code-generator
$ pip install -e .
```

# Contribute
We are waiting for your contributions to `fastapi-code-generator`.

## How to contribute

```bash
## 1. Clone your fork repository
$ git clone git@github.com:<your username>/fastapi-code-generator.git
$ cd fastapi-code-generator

## 2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
$ curl -LsSf https://astral.sh/uv/install.sh | sh

## 3. Install tox with uv
$ uv tool install --python-preference only-managed --python 3.14 tox --with tox-uv

## 4. Create a development environment
$ tox run -e dev

.tox/dev is a Python environment you can use for development purposes

## 5. Install pre-commit hooks
$ uv tool install prek
$ prek install

## 6. Create new branch and rewrite code.
$ git checkout -b new-branch

## 7. Run unittest under Python 3.14 (you should pass all tests and coverage should be 100%)
$ tox run -e py314-parallel

## 8. Format code
$ tox run -e fix

## 9. Check lint and types
$ tox run -e type

## 10. Build package metadata
$ tox run -e pkg_meta

## 11. Commit and Push...
```
