# Development

Install the package in editable mode:

```sh
$ git clone git@github.com:koxudaxi/fastapi-code-generator.git
$ poetry install fastapi-code-generator
```

# Contribute
We are waiting for your contributions to `fastapi-code-generator`.

## How to contribute

```bash
## 1. Clone your fork repository
$ git clone git@github.com:<your username>/fastapi-code-generator.git
$ cd fastapi-code-generator

## 2. Install [poetry](https://github.com/python-poetry/poetry)
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python 

## 3. Install dependencies
$ poetry install

## 4. Create new branch and rewrite code.
$ git checkout -b new-branch

## 5. Run unittest (you should pass all test and coverage should be 100%)
$ ./scripts/test.sh

## 6. Format code
$ ./scripts/format.sh

## 7. Check lint (mypy)
$ ./scripts/lint.sh

## 8. Commit and Push...
```
