[[package]]
name = "appdirs"
version = "1.4.4"
description = "A small Python module for determining appropriate platform-specific dirs, e.g. a \"user data dir\"."
category = "main"
optional = false
python-versions = "*"

[[package]]
name = "argcomplete"
version = "1.12.2"
description = "Bash tab completion for argparse"
category = "main"
optional = false
python-versions = "*"

[package.dependencies]
importlib-metadata = {version = ">=0.23,<4", markers = "python_version == \"3.7\""}

[package.extras]
test = ["coverage", "flake8", "pexpect", "wheel"]

[[package]]
name = "atomicwrites"
version = "1.4.0"
description = "Atomic file writes."
category = "dev"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*"

[[package]]
name = "attrs"
version = "20.3.0"
description = "Classes Without Boilerplate"
category = "main"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*"

[package.extras]
dev = ["coverage[toml] (>=5.0.2)", "hypothesis", "pympler", "pytest (>=4.3.0)", "six", "zope.interface", "furo", "sphinx", "pre-commit"]
docs = ["furo", "sphinx", "zope.interface"]
tests = ["coverage[toml] (>=5.0.2)", "hypothesis", "pympler", "pytest (>=4.3.0)", "six", "zope.interface"]
tests_no_zope = ["coverage[toml] (>=5.0.2)", "hypothesis", "pympler", "pytest (>=4.3.0)", "six"]

[[package]]
name = "black"
version = "19.10b0"
description = "The uncompromising code formatter."
category = "main"
optional = false
python-versions = ">=3.6"

[package.dependencies]
appdirs = "*"
attrs = ">=18.1.0"
click = ">=6.5"
pathspec = ">=0.6,<1"
regex = "*"
toml = ">=0.9.4"
typed-ast = ">=1.4.0"

[package.extras]
d = ["aiohttp (>=3.3.2)", "aiohttp-cors"]

[[package]]
name = "certifi"
version = "2020.12.5"
description = "Python package for providing Mozilla's CA Bundle."
category = "main"
optional = false
python-versions = "*"

[[package]]
name = "chardet"
version = "4.0.0"
description = "Universal encoding detector for Python 2 and 3"
category = "main"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*"

[[package]]
name = "click"
version = "7.1.2"
description = "Composable command line interface toolkit"
category = "main"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*"

[[package]]
name = "colorama"
version = "0.4.4"
description = "Cross-platform colored terminal text."
category = "main"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*"

[[package]]
name = "coverage"
version = "5.5"
description = "Code coverage measurement for Python"
category = "dev"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4"

[package.dependencies]
toml = {version = "*", optional = true, markers = "extra == \"toml\""}

[package.extras]
toml = ["toml"]

[[package]]
name = "datamodel-code-generator"
version = "0.11.5"
description = "Datamodel Code Generator"
category = "main"
optional = false
python-versions = ">=3.6.1"

[package.dependencies]
argcomplete = ">=1.10,<2.0"
black = ">=19.10b0"
genson = ">=1.2.1,<2.0"
httpx = {version = "*", optional = true, markers = "extra == \"http\""}
inflect = ">=4.1.0,<6.0"
isort = ">=4.3.21,<6.0"
jinja2 = ">=2.10.1,<3.0"
openapi-spec-validator = ">=0.2.8,<0.4"
prance = ">=0.18.2,<1.0"
pydantic = [
    {version = ">=1.5.1,<2.0", extras = ["email"], markers = "python_version < \"3.9\""},
    {version = ">=1.7.2,<2.0", extras = ["email"], markers = "python_version >= \"3.9\""},
]
PySnooper = ">=0.4.1,<1.0.0"
toml = ">=0.10.0,<1.0.0"

[package.extras]
all = ["pytest-runner", "setuptools-scm", "pytest (>=4.6)", "pytest-benchmark", "pytest-cov", "pytest-mock", "mypy", "isort", "freezegun", "httpx", "mkdocs", "mkdocs-material", "wheel", "twine", "codecov"]
ci = ["codecov"]
docs = ["mkdocs", "mkdocs-material"]
http = ["httpx"]
setup = ["pytest-runner", "setuptools-scm"]
test = ["pytest (>=4.6)", "pytest-benchmark", "pytest-cov", "pytest-mock", "mypy", "isort", "freezegun"]
wheel = ["wheel", "twine"]

[[package]]
name = "dnspython"
version = "2.1.0"
description = "DNS toolkit"
category = "main"
optional = false
python-versions = ">=3.6"

[package.extras]
dnssec = ["cryptography (>=2.6)"]
doh = ["requests", "requests-toolbelt"]
idna = ["idna (>=2.1)"]
curio = ["curio (>=1.2)", "sniffio (>=1.1)"]
trio = ["trio (>=0.14.0)", "sniffio (>=1.1)"]

[[package]]
name = "email-validator"
version = "1.1.2"
description = "A robust email syntax and deliverability validation library for Python 2.x/3.x."
category = "main"
optional = false
python-versions = "*"

[package.dependencies]
dnspython = ">=1.15.0"
idna = ">=2.0.0"

[[package]]
name = "freezegun"
version = "1.1.0"
description = "Let your Python tests travel through time"
category = "dev"
optional = false
python-versions = ">=3.5"

[package.dependencies]
python-dateutil = ">=2.7"

[[package]]
name = "genson"
version = "1.2.2"
description = "GenSON is a powerful, user-friendly JSON Schema generator."
category = "main"
optional = false
python-versions = "*"

[[package]]
name = "h11"
version = "0.12.0"
description = "A pure-Python, bring-your-own-I/O implementation of HTTP/1.1"
category = "main"
optional = false
python-versions = ">=3.6"

[[package]]
name = "httpcore"
version = "0.12.3"
description = "A minimal low-level HTTP client."
category = "main"
optional = false
python-versions = ">=3.6"

[package.dependencies]
h11 = "<1.0.0"
sniffio = ">=1.0.0,<2.0.0"

[package.extras]
http2 = ["h2 (>=3,<5)"]

[[package]]
name = "httpx"
version = "0.16.1"
description = "The next generation HTTP client."
category = "main"
optional = false
python-versions = ">=3.6"

[package.dependencies]
certifi = "*"
httpcore = ">=0.12.0,<0.13.0"
rfc3986 = {version = ">=1.3,<2", extras = ["idna2008"]}
sniffio = "*"

[package.extras]
brotli = ["brotlipy (>=0.7.0,<0.8.0)"]
http2 = ["h2 (>=3.0.0,<4.0.0)"]

[[package]]
name = "idna"
version = "2.10"
description = "Internationalized Domain Names in Applications (IDNA)"
category = "main"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*"

[[package]]
name = "importlib-metadata"
version = "3.4.0"
description = "Read metadata from Python packages"
category = "main"
optional = false
python-versions = ">=3.6"

[package.dependencies]
typing-extensions = {version = ">=3.6.4", markers = "python_version < \"3.8\""}
zipp = ">=0.5"

[package.extras]
docs = ["sphinx", "jaraco.packaging (>=8.2)", "rst.linker (>=1.9)"]
testing = ["pytest (>=3.5,!=3.7.3)", "pytest-checkdocs (>=1.2.3)", "pytest-flake8", "pytest-cov", "pytest-enabler", "packaging", "pep517", "pyfakefs", "flufl.flake8", "pytest-black (>=0.3.7)", "pytest-mypy", "importlib-resources (>=1.3)"]

[[package]]
name = "inflect"
version = "4.1.1"
description = "Correctly generate plurals, singular nouns, ordinals, indefinite articles; convert numbers to words"
category = "main"
optional = false
python-versions = ">=3.6"

[package.dependencies]
importlib-metadata = {version = "*", markers = "python_version < \"3.8\""}

[package.extras]
docs = ["sphinx", "jaraco.packaging (>=3.2)", "rst.linker (>=1.9)"]
testing = ["pytest (>=3.5,!=3.7.3)", "pytest-checkdocs (>=1.2.3)", "pytest-flake8", "pytest-cov", "jaraco.test (>=3.2.0)", "pygments", "pytest-black (>=0.3.7)", "pytest-mypy"]

[[package]]
name = "iniconfig"
version = "1.1.1"
description = "iniconfig: brain-dead simple config-ini parsing"
category = "dev"
optional = false
python-versions = "*"

[[package]]
name = "isort"
version = "4.3.21"
description = "A Python utility / library to sort Python imports."
category = "main"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*"

[package.extras]
pipfile = ["pipreqs", "requirementslib"]
pyproject = ["toml"]
requirements = ["pipreqs", "pip-api"]
xdg_home = ["appdirs (>=1.4.0)"]

[[package]]
name = "jinja2"
version = "2.11.3"
description = "A very fast and expressive template engine."
category = "main"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*"

[package.dependencies]
MarkupSafe = ">=0.23"

[package.extras]
i18n = ["Babel (>=0.8)"]

[[package]]
name = "jsonschema"
version = "3.2.0"
description = "An implementation of JSON Schema validation for Python"
category = "main"
optional = false
python-versions = "*"

[package.dependencies]
attrs = ">=17.4.0"
importlib-metadata = {version = "*", markers = "python_version < \"3.8\""}
pyrsistent = ">=0.14.0"
six = ">=1.11.0"

[package.extras]
format = ["idna", "jsonpointer (>1.13)", "rfc3987", "strict-rfc3339", "webcolors"]
format_nongpl = ["idna", "jsonpointer (>1.13)", "webcolors", "rfc3986-validator (>0.1.0)", "rfc3339-validator"]

[[package]]
name = "markupsafe"
version = "1.1.1"
description = "Safely add untrusted strings to HTML/XML markup."
category = "main"
optional = false
python-versions = ">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*"

[[package]]
name = "mypy"
version = "0.812"
description = "Optional static typing for Python"
category = "dev"
optional = false
python-versions = ">=3.5"

[package.dependencies]
mypy-extensions = ">=0.4.3,<0.5.0"
typed-ast = ">=1.4.0,<1.5.0"
typing-extensions = ">=3.7.4"

[package.extras]
dmypy = ["psutil (>=4.0)"]

[[package]]
name = "mypy-extensions"
version = "0.4.3"
description = "Experimental type system extensions for programs checked with the mypy typechecker."
category = "dev"
optional = false
python-versions = "*"

[[package]]
name = "openapi-spec-validator"
version = "0.2.9"
description = "OpenAPI 2.0 (aka Swagger) and OpenAPI 3.0.0 spec validator"
category = "main"
optional = false
python-versions = "*"

[package.dependencies]
jsonschema = "*"
PyYAML = ">=5.1"
six = "*"

[package.extras]
dev = ["pre-commit"]

[[package]]
name = "packaging"
version = "20.9"
description = "Core utilities for Python packages"
category = "dev"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*"

[package.dependencies]
pyparsing = ">=2.0.2"

[[package]]
name = "pathspec"
version = "0.8.1"
description = "Utility library for gitignore style pattern matching of file paths."
category = "main"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*"

[[package]]
name = "pluggy"
version = "0.13.1"
description = "plugin and hook calling mechanisms for python"
category = "dev"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*"

[package.dependencies]
importlib-metadata = {version = ">=0.12", markers = "python_version < \"3.8\""}

[package.extras]
dev = ["pre-commit", "tox"]

[[package]]
name = "prance"
version = "0.20.2"
description = "Resolving Swagger/OpenAPI 2.0 and 3.0.0 Parser"
category = "main"
optional = false
python-versions = "*"

[package.dependencies]
chardet = ">=4.0,<5.0"
PyYAML = ">=5.3,<6.0"
requests = ">=2.25,<3.0"
semver = ">=2.13,<3.0"
six = ">=1.15,<2.0"

[package.extras]
cli = ["click (>=7.0,<8.0)"]
dev = ["tox (>=3.21)", "bumpversion (>=0.6)", "pytest (>=6.2)", "pytest-cov (>=2.11)", "flake8 (>=3.8)", "pep8-naming (>=0.11)", "flake8-quotes (>=3.2)", "flake8-docstrings (>=1.5)", "sphinx (>=3.4)", "towncrier (>=19.2)"]
flex = ["flex (>=6.13,<7.0)"]
icu = ["PyICU (>=2.4,<3.0)"]
osv = ["openapi-spec-validator (>=0.2.1)"]
ssv = ["swagger-spec-validator (>=2.4,<3.0)"]

[[package]]
name = "py"
version = "1.10.0"
description = "library with cross-python path, ini-parsing, io, code, log facilities"
category = "dev"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*"

[[package]]
name = "pydantic"
version = "1.7.3"
description = "Data validation and settings management using python 3.6 type hinting"
category = "main"
optional = false
python-versions = ">=3.6"

[package.dependencies]
email-validator = {version = ">=1.0.3", optional = true, markers = "extra == \"email\""}

[package.extras]
dotenv = ["python-dotenv (>=0.10.4)"]
email = ["email-validator (>=1.0.3)"]
typing_extensions = ["typing-extensions (>=3.7.2)"]

[[package]]
name = "pyparsing"
version = "2.4.7"
description = "Python parsing module"
category = "dev"
optional = false
python-versions = ">=2.6, !=3.0.*, !=3.1.*, !=3.2.*"

[[package]]
name = "pyrsistent"
version = "0.17.3"
description = "Persistent/Functional/Immutable data structures"
category = "main"
optional = false
python-versions = ">=3.5"

[[package]]
name = "pysnooper"
version = "0.5.0"
description = "A poor man's debugger for Python."
category = "main"
optional = false
python-versions = "*"

[package.extras]
tests = ["pytest"]

[[package]]
name = "pytest"
version = "6.2.4"
description = "pytest: simple powerful testing with Python"
category = "dev"
optional = false
python-versions = ">=3.6"

[package.dependencies]
atomicwrites = {version = ">=1.0", markers = "sys_platform == \"win32\""}
attrs = ">=19.2.0"
colorama = {version = "*", markers = "sys_platform == \"win32\""}
importlib-metadata = {version = ">=0.12", markers = "python_version < \"3.8\""}
iniconfig = "*"
packaging = "*"
pluggy = ">=0.12,<1.0.0a1"
py = ">=1.8.2"
toml = "*"

[package.extras]
testing = ["argcomplete", "hypothesis (>=3.56)", "mock", "nose", "requests", "xmlschema"]

[[package]]
name = "pytest-cov"
version = "2.12.0"
description = "Pytest plugin for measuring coverage."
category = "dev"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*"

[package.dependencies]
coverage = {version = ">=5.2.1", extras = ["toml"]}
pytest = ">=4.6"

[package.extras]
testing = ["fields", "hunter", "process-tests (==2.0.2)", "six", "pytest-xdist", "virtualenv"]

[[package]]
name = "pytest-mock"
version = "3.6.1"
description = "Thin-wrapper around the mock package for easier use with pytest"
category = "dev"
optional = false
python-versions = ">=3.6"

[package.dependencies]
pytest = ">=5.0"

[package.extras]
dev = ["pre-commit", "tox", "pytest-asyncio"]

[[package]]
name = "python-dateutil"
version = "2.8.1"
description = "Extensions to the standard Python datetime module"
category = "dev"
optional = false
python-versions = "!=3.0.*,!=3.1.*,!=3.2.*,>=2.7"

[package.dependencies]
six = ">=1.5"

[[package]]
name = "pyyaml"
version = "5.4.1"
description = "YAML parser and emitter for Python"
category = "main"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*"

[[package]]
name = "regex"
version = "2020.11.13"
description = "Alternative regular expression module, to replace re."
category = "main"
optional = false
python-versions = "*"

[[package]]
name = "requests"
version = "2.25.1"
description = "Python HTTP for Humans."
category = "main"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*"

[package.dependencies]
certifi = ">=2017.4.17"
chardet = ">=3.0.2,<5"
idna = ">=2.5,<3"
urllib3 = ">=1.21.1,<1.27"

[package.extras]
security = ["pyOpenSSL (>=0.14)", "cryptography (>=1.3.4)"]
socks = ["PySocks (>=1.5.6,!=1.5.7)", "win-inet-pton"]

[[package]]
name = "rfc3986"
version = "1.5.0"
description = "Validating URI References per RFC 3986"
category = "main"
optional = false
python-versions = "*"

[package.dependencies]
idna = {version = "*", optional = true, markers = "extra == \"idna2008\""}

[package.extras]
idna2008 = ["idna"]

[[package]]
name = "semver"
version = "2.13.0"
description = "Python helper for Semantic Versioning (http://semver.org/)"
category = "main"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*"

[[package]]
name = "shellingham"
version = "1.4.0"
description = "Tool to Detect Surrounding Shell"
category = "main"
optional = false
python-versions = "!=3.0,!=3.1,!=3.2,!=3.3,>=2.6"

[[package]]
name = "six"
version = "1.15.0"
description = "Python 2 and 3 compatibility utilities"
category = "main"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*"

[[package]]
name = "sniffio"
version = "1.2.0"
description = "Sniff out which async library your code is running under"
category = "main"
optional = false
python-versions = ">=3.5"

[[package]]
name = "stringcase"
version = "1.2.0"
description = "String case converter."
category = "main"
optional = false
python-versions = "*"

[[package]]
name = "toml"
version = "0.10.2"
description = "Python Library for Tom's Obvious, Minimal Language"
category = "main"
optional = false
python-versions = ">=2.6, !=3.0.*, !=3.1.*, !=3.2.*"

[[package]]
name = "typed-ast"
version = "1.4.2"
description = "a fork of Python 2 and 3 ast modules with type comment support"
category = "main"
optional = false
python-versions = "*"

[[package]]
name = "typer"
version = "0.3.2"
description = "Typer, build great CLIs. Easy to code. Based on Python type hints."
category = "main"
optional = false
python-versions = ">=3.6"

[package.dependencies]
click = ">=7.1.1,<7.2.0"
colorama = {version = ">=0.4.3,<0.5.0", optional = true, markers = "extra == \"all\""}
shellingham = {version = ">=1.3.0,<2.0.0", optional = true, markers = "extra == \"all\""}

[package.extras]
test = ["pytest-xdist (>=1.32.0,<2.0.0)", "pytest-sugar (>=0.9.4,<0.10.0)", "mypy (==0.782)", "black (>=19.10b0,<20.0b0)", "isort (>=5.0.6,<6.0.0)", "shellingham (>=1.3.0,<2.0.0)", "pytest (>=4.4.0,<5.4.0)", "pytest-cov (>=2.10.0,<3.0.0)", "coverage (>=5.2,<6.0)"]
all = ["colorama (>=0.4.3,<0.5.0)", "shellingham (>=1.3.0,<2.0.0)"]
dev = ["autoflake (>=1.3.1,<2.0.0)", "flake8 (>=3.8.3,<4.0.0)"]
doc = ["mkdocs (>=1.1.2,<2.0.0)", "mkdocs-material (>=5.4.0,<6.0.0)", "markdown-include (>=0.5.1,<0.6.0)"]

[[package]]
name = "typing-extensions"
version = "3.7.4.3"
description = "Backported and Experimental Type Hints for Python 3.5+"
category = "main"
optional = false
python-versions = "*"

[[package]]
name = "urllib3"
version = "1.26.4"
description = "HTTP library with thread-safe connection pooling, file post, and more."
category = "main"
optional = false
python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4"

[package.extras]
secure = ["pyOpenSSL (>=0.14)", "cryptography (>=1.3.4)", "idna (>=2.0.0)", "certifi", "ipaddress"]
socks = ["PySocks (>=1.5.6,!=1.5.7,<2.0)"]
brotli = ["brotlipy (>=0.6.0)"]

[[package]]
name = "zipp"
version = "3.4.0"
description = "Backport of pathlib-compatible object wrapper for zip files"
category = "main"
optional = false
python-versions = ">=3.6"

[package.extras]
docs = ["sphinx", "jaraco.packaging (>=3.2)", "rst.linker (>=1.9)"]
testing = ["pytest (>=3.5,!=3.7.3)", "pytest-checkdocs (>=1.2.3)", "pytest-flake8", "pytest-cov", "jaraco.test (>=3.2.0)", "jaraco.itertools", "func-timeout", "pytest-black (>=0.3.7)", "pytest-mypy"]

[metadata]
lock-version = "1.1"
python-versions = "^3.7.0"
content-hash = "5a5efa2e5172cd4d2fbc074ce8a51362473e6787c993eaeb6368fe8ef0e6988b"

[metadata.files]
appdirs = [
    {file = "appdirs-1.4.4-py2.py3-none-any.whl", hash = "sha256:a841dacd6b99318a741b166adb07e19ee71a274450e68237b4650ca1055ab128"},
    {file = "appdirs-1.4.4.tar.gz", hash = "sha256:7d5d0167b2b1ba821647616af46a749d1c653740dd0d2415100fe26e27afdf41"},
]
argcomplete = [
    {file = "argcomplete-1.12.2-py2.py3-none-any.whl", hash = "sha256:17f01a9b9b9ece3e6b07058eae737ad6e10de8b4e149105f84614783913aba71"},
    {file = "argcomplete-1.12.2.tar.gz", hash = "sha256:de0e1282330940d52ea92a80fea2e4b9e0da1932aaa570f84d268939d1897b04"},
]
atomicwrites = [
    {file = "atomicwrites-1.4.0-py2.py3-none-any.whl", hash = "sha256:6d1784dea7c0c8d4a5172b6c620f40b6e4cbfdf96d783691f2e1302a7b88e197"},
    {file = "atomicwrites-1.4.0.tar.gz", hash = "sha256:ae70396ad1a434f9c7046fd2dd196fc04b12f9e91ffb859164193be8b6168a7a"},
]
attrs = [
    {file = "attrs-20.3.0-py2.py3-none-any.whl", hash = "sha256:31b2eced602aa8423c2aea9c76a724617ed67cf9513173fd3a4f03e3a929c7e6"},
    {file = "attrs-20.3.0.tar.gz", hash = "sha256:832aa3cde19744e49938b91fea06d69ecb9e649c93ba974535d08ad92164f700"},
]
black = [
    {file = "black-19.10b0-py36-none-any.whl", hash = "sha256:1b30e59be925fafc1ee4565e5e08abef6b03fe455102883820fe5ee2e4734e0b"},
    {file = "black-19.10b0.tar.gz", hash = "sha256:c2edb73a08e9e0e6f65a0e6af18b059b8b1cdd5bef997d7a0b181df93dc81539"},
]
certifi = [
    {file = "certifi-2020.12.5-py2.py3-none-any.whl", hash = "sha256:719a74fb9e33b9bd44cc7f3a8d94bc35e4049deebe19ba7d8e108280cfd59830"},
    {file = "certifi-2020.12.5.tar.gz", hash = "sha256:1a4995114262bffbc2413b159f2a1a480c969de6e6eb13ee966d470af86af59c"},
]
chardet = [
    {file = "chardet-4.0.0-py2.py3-none-any.whl", hash = "sha256:f864054d66fd9118f2e67044ac8981a54775ec5b67aed0441892edb553d21da5"},
    {file = "chardet-4.0.0.tar.gz", hash = "sha256:0d6f53a15db4120f2b08c94f11e7d93d2c911ee118b6b30a04ec3ee8310179fa"},
]
click = [
    {file = "click-7.1.2-py2.py3-none-any.whl", hash = "sha256:dacca89f4bfadd5de3d7489b7c8a566eee0d3676333fbb50030263894c38c0dc"},
    {file = "click-7.1.2.tar.gz", hash = "sha256:d2b5255c7c6349bc1bd1e59e08cd12acbbd63ce649f2588755783aa94dfb6b1a"},
]
colorama = [
    {file = "colorama-0.4.4-py2.py3-none-any.whl", hash = "sha256:9f47eda37229f68eee03b24b9748937c7dc3868f906e8ba69fbcbdd3bc5dc3e2"},
    {file = "colorama-0.4.4.tar.gz", hash = "sha256:5941b2b48a20143d2267e95b1c2a7603ce057ee39fd88e7329b0c292aa16869b"},
]
coverage = [
    {file = "coverage-5.5-cp27-cp27m-macosx_10_9_x86_64.whl", hash = "sha256:b6d534e4b2ab35c9f93f46229363e17f63c53ad01330df9f2d6bd1187e5eaacf"},
    {file = "coverage-5.5-cp27-cp27m-manylinux1_i686.whl", hash = "sha256:b7895207b4c843c76a25ab8c1e866261bcfe27bfaa20c192de5190121770672b"},
    {file = "coverage-5.5-cp27-cp27m-manylinux1_x86_64.whl", hash = "sha256:c2723d347ab06e7ddad1a58b2a821218239249a9e4365eaff6649d31180c1669"},
    {file = "coverage-5.5-cp27-cp27m-manylinux2010_i686.whl", hash = "sha256:900fbf7759501bc7807fd6638c947d7a831fc9fdf742dc10f02956ff7220fa90"},
    {file = "coverage-5.5-cp27-cp27m-manylinux2010_x86_64.whl", hash = "sha256:004d1880bed2d97151facef49f08e255a20ceb6f9432df75f4eef018fdd5a78c"},
    {file = "coverage-5.5-cp27-cp27m-win32.whl", hash = "sha256:06191eb60f8d8a5bc046f3799f8a07a2d7aefb9504b0209aff0b47298333302a"},
    {file = "coverage-5.5-cp27-cp27m-win_amd64.whl", hash = "sha256:7501140f755b725495941b43347ba8a2777407fc7f250d4f5a7d2a1050ba8e82"},
    {file = "coverage-5.5-cp27-cp27mu-manylinux1_i686.whl", hash = "sha256:372da284cfd642d8e08ef606917846fa2ee350f64994bebfbd3afb0040436905"},
    {file = "coverage-5.5-cp27-cp27mu-manylinux1_x86_64.whl", hash = "sha256:8963a499849a1fc54b35b1c9f162f4108017b2e6db2c46c1bed93a72262ed083"},
    {file = "coverage-5.5-cp27-cp27mu-manylinux2010_i686.whl", hash = "sha256:869a64f53488f40fa5b5b9dcb9e9b2962a66a87dab37790f3fcfb5144b996ef5"},
    {file = "coverage-5.5-cp27-cp27mu-manylinux2010_x86_64.whl", hash = "sha256:4a7697d8cb0f27399b0e393c0b90f0f1e40c82023ea4d45d22bce7032a5d7b81"},
    {file = "coverage-5.5-cp310-cp310-macosx_10_14_x86_64.whl", hash = "sha256:8d0a0725ad7c1a0bcd8d1b437e191107d457e2ec1084b9f190630a4fb1af78e6"},
    {file = "coverage-5.5-cp310-cp310-manylinux1_x86_64.whl", hash = "sha256:51cb9476a3987c8967ebab3f0fe144819781fca264f57f89760037a2ea191cb0"},
    {file = "coverage-5.5-cp310-cp310-win_amd64.whl", hash = "sha256:c0891a6a97b09c1f3e073a890514d5012eb256845c451bd48f7968ef939bf4ae"},
    {file = "coverage-5.5-cp35-cp35m-macosx_10_9_x86_64.whl", hash = "sha256:3487286bc29a5aa4b93a072e9592f22254291ce96a9fbc5251f566b6b7343cdb"},
    {file = "coverage-5.5-cp35-cp35m-manylinux1_i686.whl", hash = "sha256:deee1077aae10d8fa88cb02c845cfba9b62c55e1183f52f6ae6a2df6a2187160"},
    {file = "coverage-5.5-cp35-cp35m-manylinux1_x86_64.whl", hash = "sha256:f11642dddbb0253cc8853254301b51390ba0081750a8ac03f20ea8103f0c56b6"},
    {file = "coverage-5.5-cp35-cp35m-manylinux2010_i686.whl", hash = "sha256:6c90e11318f0d3c436a42409f2749ee1a115cd8b067d7f14c148f1ce5574d701"},
    {file = "coverage-5.5-cp35-cp35m-manylinux2010_x86_64.whl", hash = "sha256:30c77c1dc9f253283e34c27935fded5015f7d1abe83bc7821680ac444eaf7793"},
    {file = "coverage-5.5-cp35-cp35m-win32.whl", hash = "sha256:9a1ef3b66e38ef8618ce5fdc7bea3d9f45f3624e2a66295eea5e57966c85909e"},
    {file = "coverage-5.5-cp35-cp35m-win_amd64.whl", hash = "sha256:972c85d205b51e30e59525694670de6a8a89691186012535f9d7dbaa230e42c3"},
    {file = "coverage-5.5-cp36-cp36m-macosx_10_9_x86_64.whl", hash = "sha256:af0e781009aaf59e25c5a678122391cb0f345ac0ec272c7961dc5455e1c40066"},
    {file = "coverage-5.5-cp36-cp36m-manylinux1_i686.whl", hash = "sha256:74d881fc777ebb11c63736622b60cb9e4aee5cace591ce274fb69e582a12a61a"},
    {file = "coverage-5.5-cp36-cp36m-manylinux1_x86_64.whl", hash = "sha256:92b017ce34b68a7d67bd6d117e6d443a9bf63a2ecf8567bb3d8c6c7bc5014465"},
    {file = "coverage-5.5-cp36-cp36m-manylinux2010_i686.whl", hash = "sha256:d636598c8305e1f90b439dbf4f66437de4a5e3c31fdf47ad29542478c8508bbb"},
    {file = "coverage-5.5-cp36-cp36m-manylinux2010_x86_64.whl", hash = "sha256:41179b8a845742d1eb60449bdb2992196e211341818565abded11cfa90efb821"},
    {file = "coverage-5.5-cp36-cp36m-win32.whl", hash = "sha256:040af6c32813fa3eae5305d53f18875bedd079960822ef8ec067a66dd8afcd45"},
    {file = "coverage-5.5-cp36-cp36m-win_amd64.whl", hash = "sha256:5fec2d43a2cc6965edc0bb9e83e1e4b557f76f843a77a2496cbe719583ce8184"},
    {file = "coverage-5.5-cp37-cp37m-macosx_10_9_x86_64.whl", hash = "sha256:18ba8bbede96a2c3dde7b868de9dcbd55670690af0988713f0603f037848418a"},
    {file = "coverage-5.5-cp37-cp37m-manylinux1_i686.whl", hash = "sha256:2910f4d36a6a9b4214bb7038d537f015346f413a975d57ca6b43bf23d6563b53"},
    {file = "coverage-5.5-cp37-cp37m-manylinux1_x86_64.whl", hash = "sha256:f0b278ce10936db1a37e6954e15a3730bea96a0997c26d7fee88e6c396c2086d"},
    {file = "coverage-5.5-cp37-cp37m-manylinux2010_i686.whl", hash = "sha256:796c9c3c79747146ebd278dbe1e5c5c05dd6b10cc3bcb8389dfdf844f3ead638"},
    {file = "coverage-5.5-cp37-cp37m-manylinux2010_x86_64.whl", hash = "sha256:53194af30d5bad77fcba80e23a1441c71abfb3e01192034f8246e0d8f99528f3"},
    {file = "coverage-5.5-cp37-cp37m-win32.whl", hash = "sha256:184a47bbe0aa6400ed2d41d8e9ed868b8205046518c52464fde713ea06e3a74a"},
    {file = "coverage-5.5-cp37-cp37m-win_amd64.whl", hash = "sha256:2949cad1c5208b8298d5686d5a85b66aae46d73eec2c3e08c817dd3513e5848a"},
    {file = "coverage-5.5-cp38-cp38-macosx_10_9_x86_64.whl", hash = "sha256:217658ec7187497e3f3ebd901afdca1af062b42cfe3e0dafea4cced3983739f6"},
    {file = "coverage-5.5-cp38-cp38-manylinux1_i686.whl", hash = "sha256:1aa846f56c3d49205c952d8318e76ccc2ae23303351d9270ab220004c580cfe2"},
    {file = "coverage-5.5-cp38-cp38-manylinux1_x86_64.whl", hash = "sha256:24d4a7de75446be83244eabbff746d66b9240ae020ced65d060815fac3423759"},
    {file = "coverage-5.5-cp38-cp38-manylinux2010_i686.whl", hash = "sha256:d1f8bf7b90ba55699b3a5e44930e93ff0189aa27186e96071fac7dd0d06a1873"},
    {file = "coverage-5.5-cp38-cp38-manylinux2010_x86_64.whl", hash = "sha256:970284a88b99673ccb2e4e334cfb38a10aab7cd44f7457564d11898a74b62d0a"},
    {file = "coverage-5.5-cp38-cp38-win32.whl", hash = "sha256:01d84219b5cdbfc8122223b39a954820929497a1cb1422824bb86b07b74594b6"},
    {file = "coverage-5.5-cp38-cp38-win_amd64.whl", hash = "sha256:2e0d881ad471768bf6e6c2bf905d183543f10098e3b3640fc029509530091502"},
    {file = "coverage-5.5-cp39-cp39-macosx_10_9_x86_64.whl", hash = "sha256:d1f9ce122f83b2305592c11d64f181b87153fc2c2bbd3bb4a3dde8303cfb1a6b"},
    {file = "coverage-5.5-cp39-cp39-manylinux1_i686.whl", hash = "sha256:13c4ee887eca0f4c5a247b75398d4114c37882658300e153113dafb1d76de529"},
    {file = "coverage-5.5-cp39-cp39-manylinux1_x86_64.whl", hash = "sha256:52596d3d0e8bdf3af43db3e9ba8dcdaac724ba7b5ca3f6358529d56f7a166f8b"},
    {file = "coverage-5.5-cp39-cp39-manylinux2010_i686.whl", hash = "sha256:2cafbbb3af0733db200c9b5f798d18953b1a304d3f86a938367de1567f4b5bff"},
    {file = "coverage-5.5-cp39-cp39-manylinux2010_x86_64.whl", hash = "sha256:44d654437b8ddd9eee7d1eaee28b7219bec228520ff809af170488fd2fed3e2b"},
    {file = "coverage-5.5-cp39-cp39-win32.whl", hash = "sha256:d314ed732c25d29775e84a960c3c60808b682c08d86602ec2c3008e1202e3bb6"},
    {file = "coverage-5.5-cp39-cp39-win_amd64.whl", hash = "sha256:13034c4409db851670bc9acd836243aeee299949bd5673e11844befcb0149f03"},
    {file = "coverage-5.5-pp36-none-any.whl", hash = "sha256:f030f8873312a16414c0d8e1a1ddff2d3235655a2174e3648b4fa66b3f2f1079"},
    {file = "coverage-5.5-pp37-none-any.whl", hash = "sha256:2a3859cb82dcbda1cfd3e6f71c27081d18aa251d20a17d87d26d4cd216fb0af4"},
    {file = "coverage-5.5.tar.gz", hash = "sha256:ebe78fe9a0e874362175b02371bdfbee64d8edc42a044253ddf4ee7d3c15212c"},
]
datamodel-code-generator = [
    {file = "datamodel-code-generator-0.11.5.tar.gz", hash = "sha256:e0e7433a0f2567da4332c50dd14988866f434658ad4288b4c75436ace9e5b4f9"},
    {file = "datamodel_code_generator-0.11.5-py3-none-any.whl", hash = "sha256:cac3134316ba6355aa18fff810fe5b3470ae07680b23ef748a9ab786feec3374"},
]
dnspython = [
    {file = "dnspython-2.1.0-py3-none-any.whl", hash = "sha256:95d12f6ef0317118d2a1a6fc49aac65ffec7eb8087474158f42f26a639135216"},
    {file = "dnspython-2.1.0.zip", hash = "sha256:e4a87f0b573201a0f3727fa18a516b055fd1107e0e5477cded4a2de497df1dd4"},
]
email-validator = [
    {file = "email-validator-1.1.2.tar.gz", hash = "sha256:1a13bd6050d1db4475f13e444e169b6fe872434922d38968c67cea9568cce2f0"},
    {file = "email_validator-1.1.2-py2.py3-none-any.whl", hash = "sha256:094b1d1c60d790649989d38d34f69e1ef07792366277a2cf88684d03495d018f"},
]
freezegun = [
    {file = "freezegun-1.1.0-py2.py3-none-any.whl", hash = "sha256:2ae695f7eb96c62529f03a038461afe3c692db3465e215355e1bb4b0ab408712"},
    {file = "freezegun-1.1.0.tar.gz", hash = "sha256:177f9dd59861d871e27a484c3332f35a6e3f5d14626f2bf91be37891f18927f3"},
]
genson = [
    {file = "genson-1.2.2.tar.gz", hash = "sha256:8caf69aa10af7aee0e1a1351d1d06801f4696e005f06cedef438635384346a16"},
]
h11 = [
    {file = "h11-0.12.0-py3-none-any.whl", hash = "sha256:36a3cb8c0a032f56e2da7084577878a035d3b61d104230d4bd49c0c6b555a9c6"},
    {file = "h11-0.12.0.tar.gz", hash = "sha256:47222cb6067e4a307d535814917cd98fd0a57b6788ce715755fa2b6c28b56042"},
]
httpcore = [
    {file = "httpcore-0.12.3-py3-none-any.whl", hash = "sha256:93e822cd16c32016b414b789aeff4e855d0ccbfc51df563ee34d4dbadbb3bcdc"},
    {file = "httpcore-0.12.3.tar.gz", hash = "sha256:37ae835fb370049b2030c3290e12ed298bf1473c41bb72ca4aa78681eba9b7c9"},
]
httpx = [
    {file = "httpx-0.16.1-py3-none-any.whl", hash = "sha256:9cffb8ba31fac6536f2c8cde30df859013f59e4bcc5b8d43901cb3654a8e0a5b"},
    {file = "httpx-0.16.1.tar.gz", hash = "sha256:126424c279c842738805974687e0518a94c7ae8d140cd65b9c4f77ac46ffa537"},
]
idna = [
    {file = "idna-2.10-py2.py3-none-any.whl", hash = "sha256:b97d804b1e9b523befed77c48dacec60e6dcb0b5391d57af6a65a312a90648c0"},
    {file = "idna-2.10.tar.gz", hash = "sha256:b307872f855b18632ce0c21c5e45be78c0ea7ae4c15c828c20788b26921eb3f6"},
]
importlib-metadata = [
    {file = "importlib_metadata-3.4.0-py3-none-any.whl", hash = "sha256:ace61d5fc652dc280e7b6b4ff732a9c2d40db2c0f92bc6cb74e07b73d53a1771"},
    {file = "importlib_metadata-3.4.0.tar.gz", hash = "sha256:fa5daa4477a7414ae34e95942e4dd07f62adf589143c875c133c1e53c4eff38d"},
]
inflect = [
    {file = "inflect-4.1.1-py3-none-any.whl", hash = "sha256:b0d13bbb6e12313b8fc4a171c86c4f4544cf09a8498e118d25473558200bd171"},
    {file = "inflect-4.1.1.tar.gz", hash = "sha256:0527947406025991506b252620da69a5efdc72bf61aa6b4b4976e3bd71c19660"},
]
iniconfig = [
    {file = "iniconfig-1.1.1-py2.py3-none-any.whl", hash = "sha256:011e24c64b7f47f6ebd835bb12a743f2fbe9a26d4cecaa7f53bc4f35ee9da8b3"},
    {file = "iniconfig-1.1.1.tar.gz", hash = "sha256:bc3af051d7d14b2ee5ef9969666def0cd1a000e121eaea580d4a313df4b37f32"},
]
isort = [
    {file = "isort-4.3.21-py2.py3-none-any.whl", hash = "sha256:6e811fcb295968434526407adb8796944f1988c5b65e8139058f2014cbe100fd"},
    {file = "isort-4.3.21.tar.gz", hash = "sha256:54da7e92468955c4fceacd0c86bd0ec997b0e1ee80d97f67c35a78b719dccab1"},
]
jinja2 = [
    {file = "Jinja2-2.11.3-py2.py3-none-any.whl", hash = "sha256:03e47ad063331dd6a3f04a43eddca8a966a26ba0c5b7207a9a9e4e08f1b29419"},
    {file = "Jinja2-2.11.3.tar.gz", hash = "sha256:a6d58433de0ae800347cab1fa3043cebbabe8baa9d29e668f1c768cb87a333c6"},
]
jsonschema = [
    {file = "jsonschema-3.2.0-py2.py3-none-any.whl", hash = "sha256:4e5b3cf8216f577bee9ce139cbe72eca3ea4f292ec60928ff24758ce626cd163"},
    {file = "jsonschema-3.2.0.tar.gz", hash = "sha256:c8a85b28d377cc7737e46e2d9f2b4f44ee3c0e1deac6bf46ddefc7187d30797a"},
]
markupsafe = [
    {file = "MarkupSafe-1.1.1-cp27-cp27m-macosx_10_6_intel.whl", hash = "sha256:09027a7803a62ca78792ad89403b1b7a73a01c8cb65909cd876f7fcebd79b161"},
    {file = "MarkupSafe-1.1.1-cp27-cp27m-manylinux1_i686.whl", hash = "sha256:e249096428b3ae81b08327a63a485ad0878de3fb939049038579ac0ef61e17e7"},
    {file = "MarkupSafe-1.1.1-cp27-cp27m-manylinux1_x86_64.whl", hash = "sha256:500d4957e52ddc3351cabf489e79c91c17f6e0899158447047588650b5e69183"},
    {file = "MarkupSafe-1.1.1-cp27-cp27m-win32.whl", hash = "sha256:b2051432115498d3562c084a49bba65d97cf251f5a331c64a12ee7e04dacc51b"},
    {file = "MarkupSafe-1.1.1-cp27-cp27m-win_amd64.whl", hash = "sha256:98c7086708b163d425c67c7a91bad6e466bb99d797aa64f965e9d25c12111a5e"},
    {file = "MarkupSafe-1.1.1-cp27-cp27mu-manylinux1_i686.whl", hash = "sha256:cd5df75523866410809ca100dc9681e301e3c27567cf498077e8551b6d20e42f"},
    {file = "MarkupSafe-1.1.1-cp27-cp27mu-manylinux1_x86_64.whl", hash = "sha256:43a55c2930bbc139570ac2452adf3d70cdbb3cfe5912c71cdce1c2c6bbd9c5d1"},
    {file = "MarkupSafe-1.1.1-cp34-cp34m-macosx_10_6_intel.whl", hash = "sha256:1027c282dad077d0bae18be6794e6b6b8c91d58ed8a8d89a89d59693b9131db5"},
    {file = "MarkupSafe-1.1.1-cp34-cp34m-manylinux1_i686.whl", hash = "sha256:62fe6c95e3ec8a7fad637b7f3d372c15ec1caa01ab47926cfdf7a75b40e0eac1"},
    {file = "MarkupSafe-1.1.1-cp34-cp34m-manylinux1_x86_64.whl", hash = "sha256:88e5fcfb52ee7b911e8bb6d6aa2fd21fbecc674eadd44118a9cc3863f938e735"},
    {file = "MarkupSafe-1.1.1-cp34-cp34m-win32.whl", hash = "sha256:ade5e387d2ad0d7ebf59146cc00c8044acbd863725f887353a10df825fc8ae21"},
    {file = "MarkupSafe-1.1.1-cp34-cp34m-win_amd64.whl", hash = "sha256:09c4b7f37d6c648cb13f9230d847adf22f8171b1ccc4d5682398e77f40309235"},
    {file = "MarkupSafe-1.1.1-cp35-cp35m-macosx_10_6_intel.whl", hash = "sha256:79855e1c5b8da654cf486b830bd42c06e8780cea587384cf6545b7d9ac013a0b"},
    {file = "MarkupSafe-1.1.1-cp35-cp35m-manylinux1_i686.whl", hash = "sha256:c8716a48d94b06bb3b2524c2b77e055fb313aeb4ea620c8dd03a105574ba704f"},
    {file = "MarkupSafe-1.1.1-cp35-cp35m-manylinux1_x86_64.whl", hash = "sha256:7c1699dfe0cf8ff607dbdcc1e9b9af1755371f92a68f706051cc8c37d447c905"},
    {file = "MarkupSafe-1.1.1-cp35-cp35m-win32.whl", hash = "sha256:6dd73240d2af64df90aa7c4e7481e23825ea70af4b4922f8ede5b9e35f78a3b1"},
    {file = "MarkupSafe-1.1.1-cp35-cp35m-win_amd64.whl", hash = "sha256:9add70b36c5666a2ed02b43b335fe19002ee5235efd4b8a89bfcf9005bebac0d"},
    {file = "MarkupSafe-1.1.1-cp36-cp36m-macosx_10_6_intel.whl", hash = "sha256:24982cc2533820871eba85ba648cd53d8623687ff11cbb805be4ff7b4c971aff"},
    {file = "MarkupSafe-1.1.1-cp36-cp36m-macosx_10_9_x86_64.whl", hash = "sha256:d53bc011414228441014aa71dbec320c66468c1030aae3a6e29778a3382d96e5"},
    {file = "MarkupSafe-1.1.1-cp36-cp36m-manylinux1_i686.whl", hash = "sha256:00bc623926325b26bb9605ae9eae8a215691f33cae5df11ca5424f06f2d1f473"},
    {file = "MarkupSafe-1.1.1-cp36-cp36m-manylinux1_x86_64.whl", hash = "sha256:717ba8fe3ae9cc0006d7c451f0bb265ee07739daf76355d06366154ee68d221e"},
    {file = "MarkupSafe-1.1.1-cp36-cp36m-manylinux2010_i686.whl", hash = "sha256:3b8a6499709d29c2e2399569d96719a1b21dcd94410a586a18526b143ec8470f"},
    {file = "MarkupSafe-1.1.1-cp36-cp36m-manylinux2010_x86_64.whl", hash = "sha256:84dee80c15f1b560d55bcfe6d47b27d070b4681c699c572af2e3c7cc90a3b8e0"},
    {file = "MarkupSafe-1.1.1-cp36-cp36m-manylinux2014_aarch64.whl", hash = "sha256:b1dba4527182c95a0db8b6060cc98ac49b9e2f5e64320e2b56e47cb2831978c7"},
    {file = "MarkupSafe-1.1.1-cp36-cp36m-win32.whl", hash = "sha256:535f6fc4d397c1563d08b88e485c3496cf5784e927af890fb3c3aac7f933ec66"},
    {file = "MarkupSafe-1.1.1-cp36-cp36m-win_amd64.whl", hash = "sha256:b1282f8c00509d99fef04d8ba936b156d419be841854fe901d8ae224c59f0be5"},
    {file = "MarkupSafe-1.1.1-cp37-cp37m-macosx_10_6_intel.whl", hash = "sha256:8defac2f2ccd6805ebf65f5eeb132adcf2ab57aa11fdf4c0dd5169a004710e7d"},
    {file = "MarkupSafe-1.1.1-cp37-cp37m-macosx_10_9_x86_64.whl", hash = "sha256:bf5aa3cbcfdf57fa2ee9cd1822c862ef23037f5c832ad09cfea57fa846dec193"},
    {file = "MarkupSafe-1.1.1-cp37-cp37m-manylinux1_i686.whl", hash = "sha256:46c99d2de99945ec5cb54f23c8cd5689f6d7177305ebff350a58ce5f8de1669e"},
    {file = "MarkupSafe-1.1.1-cp37-cp37m-manylinux1_x86_64.whl", hash = "sha256:ba59edeaa2fc6114428f1637ffff42da1e311e29382d81b339c1817d37ec93c6"},
    {file = "MarkupSafe-1.1.1-cp37-cp37m-manylinux2010_i686.whl", hash = "sha256:6fffc775d90dcc9aed1b89219549b329a9250d918fd0b8fa8d93d154918422e1"},
    {file = "MarkupSafe-1.1.1-cp37-cp37m-manylinux2010_x86_64.whl", hash = "sha256:a6a744282b7718a2a62d2ed9d993cad6f5f585605ad352c11de459f4108df0a1"},
    {file = "MarkupSafe-1.1.1-cp37-cp37m-manylinux2014_aarch64.whl", hash = "sha256:195d7d2c4fbb0ee8139a6cf67194f3973a6b3042d742ebe0a9ed36d8b6f0c07f"},
    {file = "MarkupSafe-1.1.1-cp37-cp37m-win32.whl", hash = "sha256:b00c1de48212e4cc9603895652c5c410df699856a2853135b3967591e4beebc2"},
    {file = "MarkupSafe-1.1.1-cp37-cp37m-win_amd64.whl", hash = "sha256:9bf40443012702a1d2070043cb6291650a0841ece432556f784f004937f0f32c"},
    {file = "MarkupSafe-1.1.1-cp38-cp38-macosx_10_9_x86_64.whl", hash = "sha256:6788b695d50a51edb699cb55e35487e430fa21f1ed838122d722e0ff0ac5ba15"},
    {file = "MarkupSafe-1.1.1-cp38-cp38-manylinux1_i686.whl", hash = "sha256:cdb132fc825c38e1aeec2c8aa9338310d29d337bebbd7baa06889d09a60a1fa2"},
    {file = "MarkupSafe-1.1.1-cp38-cp38-manylinux1_x86_64.whl", hash = "sha256:13d3144e1e340870b25e7b10b98d779608c02016d5184cfb9927a9f10c689f42"},
    {file = "MarkupSafe-1.1.1-cp38-cp38-manylinux2010_i686.whl", hash = "sha256:acf08ac40292838b3cbbb06cfe9b2cb9ec78fce8baca31ddb87aaac2e2dc3bc2"},
    {file = "MarkupSafe-1.1.1-cp38-cp38-manylinux2010_x86_64.whl", hash = "sha256:d9be0ba6c527163cbed5e0857c451fcd092ce83947944d6c14bc95441203f032"},
    {file = "MarkupSafe-1.1.1-cp38-cp38-manylinux2014_aarch64.whl", hash = "sha256:caabedc8323f1e93231b52fc32bdcde6db817623d33e100708d9a68e1f53b26b"},
    {file = "MarkupSafe-1.1.1-cp38-cp38-win32.whl", hash = "sha256:596510de112c685489095da617b5bcbbac7dd6384aeebeda4df6025d0256a81b"},
    {file = "MarkupSafe-1.1.1-cp38-cp38-win_amd64.whl", hash = "sha256:e8313f01ba26fbbe36c7be1966a7b7424942f670f38e666995b88d012765b9be"},
    {file = "MarkupSafe-1.1.1-cp39-cp39-macosx_10_9_x86_64.whl", hash = "sha256:d73a845f227b0bfe8a7455ee623525ee656a9e2e749e4742706d80a6065d5e2c"},
    {file = "MarkupSafe-1.1.1-cp39-cp39-manylinux1_i686.whl", hash = "sha256:98bae9582248d6cf62321dcb52aaf5d9adf0bad3b40582925ef7c7f0ed85fceb"},
    {file = "MarkupSafe-1.1.1-cp39-cp39-manylinux1_x86_64.whl", hash = "sha256:2beec1e0de6924ea551859edb9e7679da6e4870d32cb766240ce17e0a0ba2014"},
    {file = "MarkupSafe-1.1.1-cp39-cp39-manylinux2010_i686.whl", hash = "sha256:7fed13866cf14bba33e7176717346713881f56d9d2bcebab207f7a036f41b850"},
    {file = "MarkupSafe-1.1.1-cp39-cp39-manylinux2010_x86_64.whl", hash = "sha256:6f1e273a344928347c1290119b493a1f0303c52f5a5eae5f16d74f48c15d4a85"},
    {file = "MarkupSafe-1.1.1-cp39-cp39-manylinux2014_aarch64.whl", hash = "sha256:feb7b34d6325451ef96bc0e36e1a6c0c1c64bc1fbec4b854f4529e51887b1621"},
    {file = "MarkupSafe-1.1.1-cp39-cp39-win32.whl", hash = "sha256:22c178a091fc6630d0d045bdb5992d2dfe14e3259760e713c490da5323866c39"},
    {file = "MarkupSafe-1.1.1-cp39-cp39-win_amd64.whl", hash = "sha256:b7d644ddb4dbd407d31ffb699f1d140bc35478da613b441c582aeb7c43838dd8"},
    {file = "MarkupSafe-1.1.1.tar.gz", hash = "sha256:29872e92839765e546828bb7754a68c418d927cd064fd4708fab9fe9c8bb116b"},
]
mypy = [
    {file = "mypy-0.812-cp35-cp35m-macosx_10_9_x86_64.whl", hash = "sha256:a26f8ec704e5a7423c8824d425086705e381b4f1dfdef6e3a1edab7ba174ec49"},
    {file = "mypy-0.812-cp35-cp35m-manylinux1_x86_64.whl", hash = "sha256:28fb5479c494b1bab244620685e2eb3c3f988d71fd5d64cc753195e8ed53df7c"},
    {file = "mypy-0.812-cp35-cp35m-manylinux2010_x86_64.whl", hash = "sha256:9743c91088d396c1a5a3c9978354b61b0382b4e3c440ce83cf77994a43e8c521"},
    {file = "mypy-0.812-cp35-cp35m-win_amd64.whl", hash = "sha256:d7da2e1d5f558c37d6e8c1246f1aec1e7349e4913d8fb3cb289a35de573fe2eb"},
    {file = "mypy-0.812-cp36-cp36m-macosx_10_9_x86_64.whl", hash = "sha256:4eec37370483331d13514c3f55f446fc5248d6373e7029a29ecb7b7494851e7a"},
    {file = "mypy-0.812-cp36-cp36m-manylinux1_x86_64.whl", hash = "sha256:d65cc1df038ef55a99e617431f0553cd77763869eebdf9042403e16089fe746c"},
    {file = "mypy-0.812-cp36-cp36m-manylinux2010_x86_64.whl", hash = "sha256:61a3d5b97955422964be6b3baf05ff2ce7f26f52c85dd88db11d5e03e146a3a6"},
    {file = "mypy-0.812-cp36-cp36m-win_amd64.whl", hash = "sha256:25adde9b862f8f9aac9d2d11971f226bd4c8fbaa89fb76bdadb267ef22d10064"},
    {file = "mypy-0.812-cp37-cp37m-macosx_10_9_x86_64.whl", hash = "sha256:552a815579aa1e995f39fd05dde6cd378e191b063f031f2acfe73ce9fb7f9e56"},
    {file = "mypy-0.812-cp37-cp37m-manylinux1_x86_64.whl", hash = "sha256:499c798053cdebcaa916eef8cd733e5584b5909f789de856b482cd7d069bdad8"},
    {file = "mypy-0.812-cp37-cp37m-manylinux2010_x86_64.whl", hash = "sha256:5873888fff1c7cf5b71efbe80e0e73153fe9212fafdf8e44adfe4c20ec9f82d7"},
    {file = "mypy-0.812-cp37-cp37m-win_amd64.whl", hash = "sha256:9f94aac67a2045ec719ffe6111df543bac7874cee01f41928f6969756e030564"},
    {file = "mypy-0.812-cp38-cp38-macosx_10_9_x86_64.whl", hash = "sha256:d23e0ea196702d918b60c8288561e722bf437d82cb7ef2edcd98cfa38905d506"},
    {file = "mypy-0.812-cp38-cp38-manylinux1_x86_64.whl", hash = "sha256:674e822aa665b9fd75130c6c5f5ed9564a38c6cea6a6432ce47eafb68ee578c5"},
    {file = "mypy-0.812-cp38-cp38-manylinux2010_x86_64.whl", hash = "sha256:abf7e0c3cf117c44d9285cc6128856106183938c68fd4944763003decdcfeb66"},
    {file = "mypy-0.812-cp38-cp38-win_amd64.whl", hash = "sha256:0d0a87c0e7e3a9becdfbe936c981d32e5ee0ccda3e0f07e1ef2c3d1a817cf73e"},
    {file = "mypy-0.812-cp39-cp39-macosx_10_9_x86_64.whl", hash = "sha256:7ce3175801d0ae5fdfa79b4f0cfed08807af4d075b402b7e294e6aa72af9aa2a"},
    {file = "mypy-0.812-cp39-cp39-manylinux1_x86_64.whl", hash = "sha256:b09669bcda124e83708f34a94606e01b614fa71931d356c1f1a5297ba11f110a"},
    {file = "mypy-0.812-cp39-cp39-manylinux2010_x86_64.whl", hash = "sha256:33f159443db0829d16f0a8d83d94df3109bb6dd801975fe86bacb9bf71628e97"},
    {file = "mypy-0.812-cp39-cp39-win_amd64.whl", hash = "sha256:3f2aca7f68580dc2508289c729bd49ee929a436208d2b2b6aab15745a70a57df"},
    {file = "mypy-0.812-py3-none-any.whl", hash = "sha256:2f9b3407c58347a452fc0736861593e105139b905cca7d097e413453a1d650b4"},
    {file = "mypy-0.812.tar.gz", hash = "sha256:cd07039aa5df222037005b08fbbfd69b3ab0b0bd7a07d7906de75ae52c4e3119"},
]
mypy-extensions = [
    {file = "mypy_extensions-0.4.3-py2.py3-none-any.whl", hash = "sha256:090fedd75945a69ae91ce1303b5824f428daf5a028d2f6ab8a299250a846f15d"},
    {file = "mypy_extensions-0.4.3.tar.gz", hash = "sha256:2d82818f5bb3e369420cb3c4060a7970edba416647068eb4c5343488a6c604a8"},
]
openapi-spec-validator = [
    {file = "openapi-spec-validator-0.2.9.tar.gz", hash = "sha256:79381a69b33423ee400ae1624a461dae7725e450e2e306e32f2dd8d16a4d85cb"},
    {file = "openapi_spec_validator-0.2.9-py2-none-any.whl", hash = "sha256:6dd75e50c94f1bb454d0e374a56418e7e06a07affb2c7f1df88564c5d728dac3"},
    {file = "openapi_spec_validator-0.2.9-py3-none-any.whl", hash = "sha256:ec1b01a00e20955a527358886991ae34b4b791b253027ee9f7df5f84b59d91c7"},
]
packaging = [
    {file = "packaging-20.9-py2.py3-none-any.whl", hash = "sha256:67714da7f7bc052e064859c05c595155bd1ee9f69f76557e21f051443c20947a"},
    {file = "packaging-20.9.tar.gz", hash = "sha256:5b327ac1320dc863dca72f4514ecc086f31186744b84a230374cc1fd776feae5"},
]
pathspec = [
    {file = "pathspec-0.8.1-py2.py3-none-any.whl", hash = "sha256:aa0cb481c4041bf52ffa7b0d8fa6cd3e88a2ca4879c533c9153882ee2556790d"},
    {file = "pathspec-0.8.1.tar.gz", hash = "sha256:86379d6b86d75816baba717e64b1a3a3469deb93bb76d613c9ce79edc5cb68fd"},
]
pluggy = [
    {file = "pluggy-0.13.1-py2.py3-none-any.whl", hash = "sha256:966c145cd83c96502c3c3868f50408687b38434af77734af1e9ca461a4081d2d"},
    {file = "pluggy-0.13.1.tar.gz", hash = "sha256:15b2acde666561e1298d71b523007ed7364de07029219b604cf808bfa1c765b0"},
]
prance = [
    {file = "prance-0.20.2-py2.py3-none-any.whl", hash = "sha256:dc79bf29af07d630e7d8119bad8440ab85aed49ada5a0705f08e469afeffa35f"},
    {file = "prance-0.20.2.tar.gz", hash = "sha256:4ffcddae6218cf6753a02af36ca9fb1c92eec4689441789ee2e9963230882388"},
]
py = [
    {file = "py-1.10.0-py2.py3-none-any.whl", hash = "sha256:3b80836aa6d1feeaa108e046da6423ab8f6ceda6468545ae8d02d9d58d18818a"},
    {file = "py-1.10.0.tar.gz", hash = "sha256:21b81bda15b66ef5e1a777a21c4dcd9c20ad3efd0b3f817e7a809035269e1bd3"},
]
pydantic = [
    {file = "pydantic-1.7.3-cp36-cp36m-macosx_10_9_x86_64.whl", hash = "sha256:c59ea046aea25be14dc22d69c97bee629e6d48d2b2ecb724d7fe8806bf5f61cd"},
    {file = "pydantic-1.7.3-cp36-cp36m-manylinux1_i686.whl", hash = "sha256:a4143c8d0c456a093387b96e0f5ee941a950992904d88bc816b4f0e72c9a0009"},
    {file = "pydantic-1.7.3-cp36-cp36m-manylinux2014_i686.whl", hash = "sha256:d8df4b9090b595511906fa48deda47af04e7d092318bfb291f4d45dfb6bb2127"},
    {file = "pydantic-1.7.3-cp36-cp36m-manylinux2014_x86_64.whl", hash = "sha256:514b473d264671a5c672dfb28bdfe1bf1afd390f6b206aa2ec9fed7fc592c48e"},
    {file = "pydantic-1.7.3-cp36-cp36m-win_amd64.whl", hash = "sha256:dba5c1f0a3aeea5083e75db9660935da90216f8a81b6d68e67f54e135ed5eb23"},
    {file = "pydantic-1.7.3-cp37-cp37m-macosx_10_9_x86_64.whl", hash = "sha256:59e45f3b694b05a69032a0d603c32d453a23f0de80844fb14d55ab0c6c78ff2f"},
    {file = "pydantic-1.7.3-cp37-cp37m-manylinux1_i686.whl", hash = "sha256:5b24e8a572e4b4c18f614004dda8c9f2c07328cb5b6e314d6e1bbd536cb1a6c1"},
    {file = "pydantic-1.7.3-cp37-cp37m-manylinux2014_i686.whl", hash = "sha256:b2b054d095b6431cdda2f852a6d2f0fdec77686b305c57961b4c5dd6d863bf3c"},
    {file = "pydantic-1.7.3-cp37-cp37m-manylinux2014_x86_64.whl", hash = "sha256:025bf13ce27990acc059d0c5be46f416fc9b293f45363b3d19855165fee1874f"},
    {file = "pydantic-1.7.3-cp37-cp37m-win_amd64.whl", hash = "sha256:6e3874aa7e8babd37b40c4504e3a94cc2023696ced5a0500949f3347664ff8e2"},
    {file = "pydantic-1.7.3-cp38-cp38-macosx_10_9_x86_64.whl", hash = "sha256:e682f6442ebe4e50cb5e1cfde7dda6766fb586631c3e5569f6aa1951fd1a76ef"},
    {file = "pydantic-1.7.3-cp38-cp38-manylinux1_i686.whl", hash = "sha256:185e18134bec5ef43351149fe34fda4758e53d05bb8ea4d5928f0720997b79ef"},
    {file = "pydantic-1.7.3-cp38-cp38-manylinux2014_i686.whl", hash = "sha256:f5b06f5099e163295b8ff5b1b71132ecf5866cc6e7f586d78d7d3fd6e8084608"},
    {file = "pydantic-1.7.3-cp38-cp38-manylinux2014_x86_64.whl", hash = "sha256:24ca47365be2a5a3cc3f4a26dcc755bcdc9f0036f55dcedbd55663662ba145ec"},
    {file = "pydantic-1.7.3-cp38-cp38-win_amd64.whl", hash = "sha256:d1fe3f0df8ac0f3a9792666c69a7cd70530f329036426d06b4f899c025aca74e"},
    {file = "pydantic-1.7.3-cp39-cp39-macosx_10_9_x86_64.whl", hash = "sha256:f6864844b039805add62ebe8a8c676286340ba0c6d043ae5dea24114b82a319e"},
    {file = "pydantic-1.7.3-cp39-cp39-manylinux1_i686.whl", hash = "sha256:ecb54491f98544c12c66ff3d15e701612fc388161fd455242447083350904730"},
    {file = "pydantic-1.7.3-cp39-cp39-manylinux2014_i686.whl", hash = "sha256:ffd180ebd5dd2a9ac0da4e8b995c9c99e7c74c31f985ba090ee01d681b1c4b95"},
    {file = "pydantic-1.7.3-cp39-cp39-manylinux2014_x86_64.whl", hash = "sha256:8d72e814c7821125b16f1553124d12faba88e85405b0864328899aceaad7282b"},
    {file = "pydantic-1.7.3-cp39-cp39-win_amd64.whl", hash = "sha256:475f2fa134cf272d6631072554f845d0630907fce053926ff634cc6bc45bf1af"},
    {file = "pydantic-1.7.3-py3-none-any.whl", hash = "sha256:38be427ea01a78206bcaf9a56f835784afcba9e5b88fbdce33bbbfbcd7841229"},
    {file = "pydantic-1.7.3.tar.gz", hash = "sha256:213125b7e9e64713d16d988d10997dabc6a1f73f3991e1ff8e35ebb1409c7dc9"},
]
pyparsing = [
    {file = "pyparsing-2.4.7-py2.py3-none-any.whl", hash = "sha256:ef9d7589ef3c200abe66653d3f1ab1033c3c419ae9b9bdb1240a85b024efc88b"},
    {file = "pyparsing-2.4.7.tar.gz", hash = "sha256:c203ec8783bf771a155b207279b9bccb8dea02d8f0c9e5f8ead507bc3246ecc1"},
]
pyrsistent = [
    {file = "pyrsistent-0.17.3.tar.gz", hash = "sha256:2e636185d9eb976a18a8a8e96efce62f2905fea90041958d8cc2a189756ebf3e"},
]
pysnooper = [
    {file = "PySnooper-0.5.0-py2.py3-none-any.whl", hash = "sha256:7280fd86cd1da732fade981e00998bf01be39e9e4a58b418469f47203cc329b1"},
    {file = "PySnooper-0.5.0.tar.gz", hash = "sha256:ec3c4648dbe3bc848a0ecea5e2ffea3a5947797599afb627a68ac4e44454116b"},
]
pytest = [
    {file = "pytest-6.2.4-py3-none-any.whl", hash = "sha256:91ef2131a9bd6be8f76f1f08eac5c5317221d6ad1e143ae03894b862e8976890"},
    {file = "pytest-6.2.4.tar.gz", hash = "sha256:50bcad0a0b9c5a72c8e4e7c9855a3ad496ca6a881a3641b4260605450772c54b"},
]
pytest-cov = [
    {file = "pytest-cov-2.12.0.tar.gz", hash = "sha256:8535764137fecce504a49c2b742288e3d34bc09eed298ad65963616cc98fd45e"},
    {file = "pytest_cov-2.12.0-py2.py3-none-any.whl", hash = "sha256:95d4933dcbbacfa377bb60b29801daa30d90c33981ab2a79e9ab4452c165066e"},
]
pytest-mock = [
    {file = "pytest-mock-3.6.1.tar.gz", hash = "sha256:40217a058c52a63f1042f0784f62009e976ba824c418cced42e88d5f40ab0e62"},
    {file = "pytest_mock-3.6.1-py3-none-any.whl", hash = "sha256:30c2f2cc9759e76eee674b81ea28c9f0b94f8f0445a1b87762cadf774f0df7e3"},
]
python-dateutil = [
    {file = "python-dateutil-2.8.1.tar.gz", hash = "sha256:73ebfe9dbf22e832286dafa60473e4cd239f8592f699aa5adaf10050e6e1823c"},
    {file = "python_dateutil-2.8.1-py2.py3-none-any.whl", hash = "sha256:75bb3f31ea686f1197762692a9ee6a7550b59fc6ca3a1f4b5d7e32fb98e2da2a"},
]
pyyaml = [
    {file = "PyYAML-5.4.1-cp27-cp27m-macosx_10_9_x86_64.whl", hash = "sha256:3b2b1824fe7112845700f815ff6a489360226a5609b96ec2190a45e62a9fc922"},
    {file = "PyYAML-5.4.1-cp27-cp27m-win32.whl", hash = "sha256:129def1b7c1bf22faffd67b8f3724645203b79d8f4cc81f674654d9902cb4393"},
    {file = "PyYAML-5.4.1-cp27-cp27m-win_amd64.whl", hash = "sha256:4465124ef1b18d9ace298060f4eccc64b0850899ac4ac53294547536533800c8"},
    {file = "PyYAML-5.4.1-cp27-cp27mu-manylinux1_x86_64.whl", hash = "sha256:bb4191dfc9306777bc594117aee052446b3fa88737cd13b7188d0e7aa8162185"},
    {file = "PyYAML-5.4.1-cp36-cp36m-macosx_10_9_x86_64.whl", hash = "sha256:6c78645d400265a062508ae399b60b8c167bf003db364ecb26dcab2bda048253"},
    {file = "PyYAML-5.4.1-cp36-cp36m-manylinux1_x86_64.whl", hash = "sha256:4e0583d24c881e14342eaf4ec5fbc97f934b999a6828693a99157fde912540cc"},
    {file = "PyYAML-5.4.1-cp36-cp36m-manylinux2014_aarch64.whl", hash = "sha256:72a01f726a9c7851ca9bfad6fd09ca4e090a023c00945ea05ba1638c09dc3347"},
    {file = "PyYAML-5.4.1-cp36-cp36m-manylinux2014_s390x.whl", hash = "sha256:895f61ef02e8fed38159bb70f7e100e00f471eae2bc838cd0f4ebb21e28f8541"},
    {file = "PyYAML-5.4.1-cp36-cp36m-win32.whl", hash = "sha256:3bd0e463264cf257d1ffd2e40223b197271046d09dadf73a0fe82b9c1fc385a5"},
    {file = "PyYAML-5.4.1-cp36-cp36m-win_amd64.whl", hash = "sha256:e4fac90784481d221a8e4b1162afa7c47ed953be40d31ab4629ae917510051df"},
    {file = "PyYAML-5.4.1-cp37-cp37m-macosx_10_9_x86_64.whl", hash = "sha256:5accb17103e43963b80e6f837831f38d314a0495500067cb25afab2e8d7a4018"},
    {file = "PyYAML-5.4.1-cp37-cp37m-manylinux1_x86_64.whl", hash = "sha256:e1d4970ea66be07ae37a3c2e48b5ec63f7ba6804bdddfdbd3cfd954d25a82e63"},
    {file = "PyYAML-5.4.1-cp37-cp37m-manylinux2014_aarch64.whl", hash = "sha256:cb333c16912324fd5f769fff6bc5de372e9e7a202247b48870bc251ed40239aa"},
    {file = "PyYAML-5.4.1-cp37-cp37m-manylinux2014_s390x.whl", hash = "sha256:fe69978f3f768926cfa37b867e3843918e012cf83f680806599ddce33c2c68b0"},
    {file = "PyYAML-5.4.1-cp37-cp37m-win32.whl", hash = "sha256:dd5de0646207f053eb0d6c74ae45ba98c3395a571a2891858e87df7c9b9bd51b"},
    {file = "PyYAML-5.4.1-cp37-cp37m-win_amd64.whl", hash = "sha256:08682f6b72c722394747bddaf0aa62277e02557c0fd1c42cb853016a38f8dedf"},
    {file = "PyYAML-5.4.1-cp38-cp38-macosx_10_9_x86_64.whl", hash = "sha256:d2d9808ea7b4af864f35ea216be506ecec180628aced0704e34aca0b040ffe46"},
    {file = "PyYAML-5.4.1-cp38-cp38-manylinux1_x86_64.whl", hash = "sha256:8c1be557ee92a20f184922c7b6424e8ab6691788e6d86137c5d93c1a6ec1b8fb"},
    {file = "PyYAML-5.4.1-cp38-cp38-manylinux2014_aarch64.whl", hash = "sha256:fd7f6999a8070df521b6384004ef42833b9bd62cfee11a09bda1079b4b704247"},
    {file = "PyYAML-5.4.1-cp38-cp38-manylinux2014_s390x.whl", hash = "sha256:bfb51918d4ff3d77c1c856a9699f8492c612cde32fd3bcd344af9be34999bfdc"},
    {file = "PyYAML-5.4.1-cp38-cp38-win32.whl", hash = "sha256:fa5ae20527d8e831e8230cbffd9f8fe952815b2b7dae6ffec25318803a7528fc"},
    {file = "PyYAML-5.4.1-cp38-cp38-win_amd64.whl", hash = "sha256:0f5f5786c0e09baddcd8b4b45f20a7b5d61a7e7e99846e3c799b05c7c53fa696"},
    {file = "PyYAML-5.4.1-cp39-cp39-macosx_10_9_x86_64.whl", hash = "sha256:294db365efa064d00b8d1ef65d8ea2c3426ac366c0c4368d930bf1c5fb497f77"},
    {file = "PyYAML-5.4.1-cp39-cp39-manylinux1_x86_64.whl", hash = "sha256:74c1485f7707cf707a7aef42ef6322b8f97921bd89be2ab6317fd782c2d53183"},
    {file = "PyYAML-5.4.1-cp39-cp39-manylinux2014_aarch64.whl", hash = "sha256:d483ad4e639292c90170eb6f7783ad19490e7a8defb3e46f97dfe4bacae89122"},
    {file = "PyYAML-5.4.1-cp39-cp39-manylinux2014_s390x.whl", hash = "sha256:fdc842473cd33f45ff6bce46aea678a54e3d21f1b61a7750ce3c498eedfe25d6"},
    {file = "PyYAML-5.4.1-cp39-cp39-win32.whl", hash = "sha256:49d4cdd9065b9b6e206d0595fee27a96b5dd22618e7520c33204a4a3239d5b10"},
    {file = "PyYAML-5.4.1-cp39-cp39-win_amd64.whl", hash = "sha256:c20cfa2d49991c8b4147af39859b167664f2ad4561704ee74c1de03318e898db"},
    {file = "PyYAML-5.4.1.tar.gz", hash = "sha256:607774cbba28732bfa802b54baa7484215f530991055bb562efbed5b2f20a45e"},
]
regex = [
    {file = "regex-2020.11.13-cp36-cp36m-macosx_10_9_x86_64.whl", hash = "sha256:8b882a78c320478b12ff024e81dc7d43c1462aa4a3341c754ee65d857a521f85"},
    {file = "regex-2020.11.13-cp36-cp36m-manylinux1_i686.whl", hash = "sha256:a63f1a07932c9686d2d416fb295ec2c01ab246e89b4d58e5fa468089cab44b70"},
    {file = "regex-2020.11.13-cp36-cp36m-manylinux1_x86_64.whl", hash = "sha256:6e4b08c6f8daca7d8f07c8d24e4331ae7953333dbd09c648ed6ebd24db5a10ee"},
    {file = "regex-2020.11.13-cp36-cp36m-manylinux2010_i686.whl", hash = "sha256:bba349276b126947b014e50ab3316c027cac1495992f10e5682dc677b3dfa0c5"},
    {file = "regex-2020.11.13-cp36-cp36m-manylinux2010_x86_64.whl", hash = "sha256:56e01daca75eae420bce184edd8bb341c8eebb19dd3bce7266332258f9fb9dd7"},
    {file = "regex-2020.11.13-cp36-cp36m-manylinux2014_aarch64.whl", hash = "sha256:6a8ce43923c518c24a2579fda49f093f1397dad5d18346211e46f134fc624e31"},
    {file = "regex-2020.11.13-cp36-cp36m-manylinux2014_i686.whl", hash = "sha256:1ab79fcb02b930de09c76d024d279686ec5d532eb814fd0ed1e0051eb8bd2daa"},
    {file = "regex-2020.11.13-cp36-cp36m-manylinux2014_x86_64.whl", hash = "sha256:9801c4c1d9ae6a70aeb2128e5b4b68c45d4f0af0d1535500884d644fa9b768c6"},
    {file = "regex-2020.11.13-cp36-cp36m-win32.whl", hash = "sha256:49cae022fa13f09be91b2c880e58e14b6da5d10639ed45ca69b85faf039f7a4e"},
    {file = "regex-2020.11.13-cp36-cp36m-win_amd64.whl", hash = "sha256:749078d1eb89484db5f34b4012092ad14b327944ee7f1c4f74d6279a6e4d1884"},
    {file = "regex-2020.11.13-cp37-cp37m-macosx_10_9_x86_64.whl", hash = "sha256:b2f4007bff007c96a173e24dcda236e5e83bde4358a557f9ccf5e014439eae4b"},
    {file = "regex-2020.11.13-cp37-cp37m-manylinux1_i686.whl", hash = "sha256:38c8fd190db64f513fe4e1baa59fed086ae71fa45083b6936b52d34df8f86a88"},
    {file = "regex-2020.11.13-cp37-cp37m-manylinux1_x86_64.whl", hash = "sha256:5862975b45d451b6db51c2e654990c1820523a5b07100fc6903e9c86575202a0"},
    {file = "regex-2020.11.13-cp37-cp37m-manylinux2010_i686.whl", hash = "sha256:262c6825b309e6485ec2493ffc7e62a13cf13fb2a8b6d212f72bd53ad34118f1"},
    {file = "regex-2020.11.13-cp37-cp37m-manylinux2010_x86_64.whl", hash = "sha256:bafb01b4688833e099d79e7efd23f99172f501a15c44f21ea2118681473fdba0"},
    {file = "regex-2020.11.13-cp37-cp37m-manylinux2014_aarch64.whl", hash = "sha256:e32f5f3d1b1c663af7f9c4c1e72e6ffe9a78c03a31e149259f531e0fed826512"},
    {file = "regex-2020.11.13-cp37-cp37m-manylinux2014_i686.whl", hash = "sha256:3bddc701bdd1efa0d5264d2649588cbfda549b2899dc8d50417e47a82e1387ba"},
    {file = "regex-2020.11.13-cp37-cp37m-manylinux2014_x86_64.whl", hash = "sha256:02951b7dacb123d8ea6da44fe45ddd084aa6777d4b2454fa0da61d569c6fa538"},
    {file = "regex-2020.11.13-cp37-cp37m-win32.whl", hash = "sha256:0d08e71e70c0237883d0bef12cad5145b84c3705e9c6a588b2a9c7080e5af2a4"},
    {file = "regex-2020.11.13-cp37-cp37m-win_amd64.whl", hash = "sha256:1fa7ee9c2a0e30405e21031d07d7ba8617bc590d391adfc2b7f1e8b99f46f444"},
    {file = "regex-2020.11.13-cp38-cp38-macosx_10_9_x86_64.whl", hash = "sha256:baf378ba6151f6e272824b86a774326f692bc2ef4cc5ce8d5bc76e38c813a55f"},
    {file = "regex-2020.11.13-cp38-cp38-manylinux1_i686.whl", hash = "sha256:e3faaf10a0d1e8e23a9b51d1900b72e1635c2d5b0e1bea1c18022486a8e2e52d"},
    {file = "regex-2020.11.13-cp38-cp38-manylinux1_x86_64.whl", hash = "sha256:2a11a3e90bd9901d70a5b31d7dd85114755a581a5da3fc996abfefa48aee78af"},
    {file = "regex-2020.11.13-cp38-cp38-manylinux2010_i686.whl", hash = "sha256:d1ebb090a426db66dd80df8ca85adc4abfcbad8a7c2e9a5ec7513ede522e0a8f"},
    {file = "regex-2020.11.13-cp38-cp38-manylinux2010_x86_64.whl", hash = "sha256:b2b1a5ddae3677d89b686e5c625fc5547c6e492bd755b520de5332773a8af06b"},
    {file = "regex-2020.11.13-cp38-cp38-manylinux2014_aarch64.whl", hash = "sha256:2c99e97d388cd0a8d30f7c514d67887d8021541b875baf09791a3baad48bb4f8"},
    {file = "regex-2020.11.13-cp38-cp38-manylinux2014_i686.whl", hash = "sha256:c084582d4215593f2f1d28b65d2a2f3aceff8342aa85afd7be23a9cad74a0de5"},
    {file = "regex-2020.11.13-cp38-cp38-manylinux2014_x86_64.whl", hash = "sha256:a3d748383762e56337c39ab35c6ed4deb88df5326f97a38946ddd19028ecce6b"},
    {file = "regex-2020.11.13-cp38-cp38-win32.whl", hash = "sha256:7913bd25f4ab274ba37bc97ad0e21c31004224ccb02765ad984eef43e04acc6c"},
    {file = "regex-2020.11.13-cp38-cp38-win_amd64.whl", hash = "sha256:6c54ce4b5d61a7129bad5c5dc279e222afd00e721bf92f9ef09e4fae28755683"},
    {file = "regex-2020.11.13-cp39-cp39-macosx_10_9_x86_64.whl", hash = "sha256:1862a9d9194fae76a7aaf0150d5f2a8ec1da89e8b55890b1786b8f88a0f619dc"},
    {file = "regex-2020.11.13-cp39-cp39-manylinux1_i686.whl", hash = "sha256:4902e6aa086cbb224241adbc2f06235927d5cdacffb2425c73e6570e8d862364"},
    {file = "regex-2020.11.13-cp39-cp39-manylinux1_x86_64.whl", hash = "sha256:7a25fcbeae08f96a754b45bdc050e1fb94b95cab046bf56b016c25e9ab127b3e"},
    {file = "regex-2020.11.13-cp39-cp39-manylinux2010_i686.whl", hash = "sha256:d2d8ce12b7c12c87e41123997ebaf1a5767a5be3ec545f64675388970f415e2e"},
    {file = "regex-2020.11.13-cp39-cp39-manylinux2010_x86_64.whl", hash = "sha256:f7d29a6fc4760300f86ae329e3b6ca28ea9c20823df123a2ea8693e967b29917"},
    {file = "regex-2020.11.13-cp39-cp39-manylinux2014_aarch64.whl", hash = "sha256:717881211f46de3ab130b58ec0908267961fadc06e44f974466d1887f865bd5b"},
    {file = "regex-2020.11.13-cp39-cp39-manylinux2014_i686.whl", hash = "sha256:3128e30d83f2e70b0bed9b2a34e92707d0877e460b402faca908c6667092ada9"},
    {file = "regex-2020.11.13-cp39-cp39-manylinux2014_x86_64.whl", hash = "sha256:8f6a2229e8ad946e36815f2a03386bb8353d4bde368fdf8ca5f0cb97264d3b5c"},
    {file = "regex-2020.11.13-cp39-cp39-win32.whl", hash = "sha256:f8f295db00ef5f8bae530fc39af0b40486ca6068733fb860b42115052206466f"},
    {file = "regex-2020.11.13-cp39-cp39-win_amd64.whl", hash = "sha256:a15f64ae3a027b64496a71ab1f722355e570c3fac5ba2801cafce846bf5af01d"},
    {file = "regex-2020.11.13.tar.gz", hash = "sha256:83d6b356e116ca119db8e7c6fc2983289d87b27b3fac238cfe5dca529d884562"},
]
requests = [
    {file = "requests-2.25.1-py2.py3-none-any.whl", hash = "sha256:c210084e36a42ae6b9219e00e48287def368a26d03a048ddad7bfee44f75871e"},
    {file = "requests-2.25.1.tar.gz", hash = "sha256:27973dd4a904a4f13b263a19c866c13b92a39ed1c964655f025f3f8d3d75b804"},
]
rfc3986 = [
    {file = "rfc3986-1.5.0-py2.py3-none-any.whl", hash = "sha256:a86d6e1f5b1dc238b218b012df0aa79409667bb209e58da56d0b94704e712a97"},
    {file = "rfc3986-1.5.0.tar.gz", hash = "sha256:270aaf10d87d0d4e095063c65bf3ddbc6ee3d0b226328ce21e036f946e421835"},
]
semver = [
    {file = "semver-2.13.0-py2.py3-none-any.whl", hash = "sha256:ced8b23dceb22134307c1b8abfa523da14198793d9787ac838e70e29e77458d4"},
    {file = "semver-2.13.0.tar.gz", hash = "sha256:fa0fe2722ee1c3f57eac478820c3a5ae2f624af8264cbdf9000c980ff7f75e3f"},
]
shellingham = [
    {file = "shellingham-1.4.0-py2.py3-none-any.whl", hash = "sha256:536b67a0697f2e4af32ab176c00a50ac2899c5a05e0d8e2dadac8e58888283f9"},
    {file = "shellingham-1.4.0.tar.gz", hash = "sha256:4855c2458d6904829bd34c299f11fdeed7cfefbf8a2c522e4caea6cd76b3171e"},
]
six = [
    {file = "six-1.15.0-py2.py3-none-any.whl", hash = "sha256:8b74bedcbbbaca38ff6d7491d76f2b06b3592611af620f8426e82dddb04a5ced"},
    {file = "six-1.15.0.tar.gz", hash = "sha256:30639c035cdb23534cd4aa2dd52c3bf48f06e5f4a941509c8bafd8ce11080259"},
]
sniffio = [
    {file = "sniffio-1.2.0-py3-none-any.whl", hash = "sha256:471b71698eac1c2112a40ce2752bb2f4a4814c22a54a3eed3676bc0f5ca9f663"},
    {file = "sniffio-1.2.0.tar.gz", hash = "sha256:c4666eecec1d3f50960c6bdf61ab7bc350648da6c126e3cf6898d8cd4ddcd3de"},
]
stringcase = [
    {file = "stringcase-1.2.0.tar.gz", hash = "sha256:48a06980661908efe8d9d34eab2b6c13aefa2163b3ced26972902e3bdfd87008"},
]
toml = [
    {file = "toml-0.10.2-py2.py3-none-any.whl", hash = "sha256:806143ae5bfb6a3c6e736a764057db0e6a0e05e338b5630894a5f779cabb4f9b"},
    {file = "toml-0.10.2.tar.gz", hash = "sha256:b3bda1d108d5dd99f4a20d24d9c348e91c4db7ab1b749200bded2f839ccbe68f"},
]
typed-ast = [
    {file = "typed_ast-1.4.2-cp35-cp35m-manylinux1_i686.whl", hash = "sha256:7703620125e4fb79b64aa52427ec192822e9f45d37d4b6625ab37ef403e1df70"},
    {file = "typed_ast-1.4.2-cp35-cp35m-manylinux1_x86_64.whl", hash = "sha256:c9aadc4924d4b5799112837b226160428524a9a45f830e0d0f184b19e4090487"},
    {file = "typed_ast-1.4.2-cp35-cp35m-manylinux2014_aarch64.whl", hash = "sha256:9ec45db0c766f196ae629e509f059ff05fc3148f9ffd28f3cfe75d4afb485412"},
    {file = "typed_ast-1.4.2-cp35-cp35m-win32.whl", hash = "sha256:85f95aa97a35bdb2f2f7d10ec5bbdac0aeb9dafdaf88e17492da0504de2e6400"},
    {file = "typed_ast-1.4.2-cp35-cp35m-win_amd64.whl", hash = "sha256:9044ef2df88d7f33692ae3f18d3be63dec69c4fb1b5a4a9ac950f9b4ba571606"},
    {file = "typed_ast-1.4.2-cp36-cp36m-macosx_10_9_x86_64.whl", hash = "sha256:c1c876fd795b36126f773db9cbb393f19808edd2637e00fd6caba0e25f2c7b64"},
    {file = "typed_ast-1.4.2-cp36-cp36m-manylinux1_i686.whl", hash = "sha256:5dcfc2e264bd8a1db8b11a892bd1647154ce03eeba94b461effe68790d8b8e07"},
    {file = "typed_ast-1.4.2-cp36-cp36m-manylinux1_x86_64.whl", hash = "sha256:8db0e856712f79c45956da0c9a40ca4246abc3485ae0d7ecc86a20f5e4c09abc"},
    {file = "typed_ast-1.4.2-cp36-cp36m-manylinux2014_aarch64.whl", hash = "sha256:d003156bb6a59cda9050e983441b7fa2487f7800d76bdc065566b7d728b4581a"},
    {file = "typed_ast-1.4.2-cp36-cp36m-win32.whl", hash = "sha256:4c790331247081ea7c632a76d5b2a265e6d325ecd3179d06e9cf8d46d90dd151"},
    {file = "typed_ast-1.4.2-cp36-cp36m-win_amd64.whl", hash = "sha256:d175297e9533d8d37437abc14e8a83cbc68af93cc9c1c59c2c292ec59a0697a3"},
    {file = "typed_ast-1.4.2-cp37-cp37m-macosx_10_9_x86_64.whl", hash = "sha256:cf54cfa843f297991b7388c281cb3855d911137223c6b6d2dd82a47ae5125a41"},
    {file = "typed_ast-1.4.2-cp37-cp37m-manylinux1_i686.whl", hash = "sha256:b4fcdcfa302538f70929eb7b392f536a237cbe2ed9cba88e3bf5027b39f5f77f"},
    {file = "typed_ast-1.4.2-cp37-cp37m-manylinux1_x86_64.whl", hash = "sha256:987f15737aba2ab5f3928c617ccf1ce412e2e321c77ab16ca5a293e7bbffd581"},
    {file = "typed_ast-1.4.2-cp37-cp37m-manylinux2014_aarch64.whl", hash = "sha256:37f48d46d733d57cc70fd5f30572d11ab8ed92da6e6b28e024e4a3edfb456e37"},
    {file = "typed_ast-1.4.2-cp37-cp37m-win32.whl", hash = "sha256:36d829b31ab67d6fcb30e185ec996e1f72b892255a745d3a82138c97d21ed1cd"},
    {file = "typed_ast-1.4.2-cp37-cp37m-win_amd64.whl", hash = "sha256:8368f83e93c7156ccd40e49a783a6a6850ca25b556c0fa0240ed0f659d2fe496"},
    {file = "typed_ast-1.4.2-cp38-cp38-macosx_10_9_x86_64.whl", hash = "sha256:963c80b583b0661918718b095e02303d8078950b26cc00b5e5ea9ababe0de1fc"},
    {file = "typed_ast-1.4.2-cp38-cp38-manylinux1_i686.whl", hash = "sha256:e683e409e5c45d5c9082dc1daf13f6374300806240719f95dc783d1fc942af10"},
    {file = "typed_ast-1.4.2-cp38-cp38-manylinux1_x86_64.whl", hash = "sha256:84aa6223d71012c68d577c83f4e7db50d11d6b1399a9c779046d75e24bed74ea"},
    {file = "typed_ast-1.4.2-cp38-cp38-manylinux2014_aarch64.whl", hash = "sha256:a38878a223bdd37c9709d07cd357bb79f4c760b29210e14ad0fb395294583787"},
    {file = "typed_ast-1.4.2-cp38-cp38-win32.whl", hash = "sha256:a2c927c49f2029291fbabd673d51a2180038f8cd5a5b2f290f78c4516be48be2"},
    {file = "typed_ast-1.4.2-cp38-cp38-win_amd64.whl", hash = "sha256:c0c74e5579af4b977c8b932f40a5464764b2f86681327410aa028a22d2f54937"},
    {file = "typed_ast-1.4.2-cp39-cp39-macosx_10_9_x86_64.whl", hash = "sha256:07d49388d5bf7e863f7fa2f124b1b1d89d8aa0e2f7812faff0a5658c01c59aa1"},
    {file = "typed_ast-1.4.2-cp39-cp39-manylinux1_i686.whl", hash = "sha256:240296b27397e4e37874abb1df2a608a92df85cf3e2a04d0d4d61055c8305ba6"},
    {file = "typed_ast-1.4.2-cp39-cp39-manylinux1_x86_64.whl", hash = "sha256:d746a437cdbca200622385305aedd9aef68e8a645e385cc483bdc5e488f07166"},
    {file = "typed_ast-1.4.2-cp39-cp39-manylinux2014_aarch64.whl", hash = "sha256:14bf1522cdee369e8f5581238edac09150c765ec1cb33615855889cf33dcb92d"},
    {file = "typed_ast-1.4.2-cp39-cp39-win32.whl", hash = "sha256:cc7b98bf58167b7f2db91a4327da24fb93368838eb84a44c472283778fc2446b"},
    {file = "typed_ast-1.4.2-cp39-cp39-win_amd64.whl", hash = "sha256:7147e2a76c75f0f64c4319886e7639e490fee87c9d25cb1d4faef1d8cf83a440"},
    {file = "typed_ast-1.4.2.tar.gz", hash = "sha256:9fc0b3cb5d1720e7141d103cf4819aea239f7d136acf9ee4a69b047b7986175a"},
]
typer = [
    {file = "typer-0.3.2-py3-none-any.whl", hash = "sha256:ba58b920ce851b12a2d790143009fa00ac1d05b3ff3257061ff69dbdfc3d161b"},
    {file = "typer-0.3.2.tar.gz", hash = "sha256:5455d750122cff96745b0dec87368f56d023725a7ebc9d2e54dd23dc86816303"},
]
typing-extensions = [
    {file = "typing_extensions-3.7.4.3-py2-none-any.whl", hash = "sha256:dafc7639cde7f1b6e1acc0f457842a83e722ccca8eef5270af2d74792619a89f"},
    {file = "typing_extensions-3.7.4.3-py3-none-any.whl", hash = "sha256:7cb407020f00f7bfc3cb3e7881628838e69d8f3fcab2f64742a5e76b2f841918"},
    {file = "typing_extensions-3.7.4.3.tar.gz", hash = "sha256:99d4073b617d30288f569d3f13d2bd7548c3a7e4c8de87db09a9d29bb3a4a60c"},
]
urllib3 = [
    {file = "urllib3-1.26.4-py2.py3-none-any.whl", hash = "sha256:2f4da4594db7e1e110a944bb1b551fdf4e6c136ad42e4234131391e21eb5b0df"},
    {file = "urllib3-1.26.4.tar.gz", hash = "sha256:e7b021f7241115872f92f43c6508082facffbd1c048e3c6e2bb9c2a157e28937"},
]
zipp = [
    {file = "zipp-3.4.0-py3-none-any.whl", hash = "sha256:102c24ef8f171fd729d46599845e95c7ab894a4cf45f5de11a44cc7444fb1108"},
    {file = "zipp-3.4.0.tar.gz", hash = "sha256:ed5eee1974372595f9e416cc7bbeeb12335201d8081ca8a0743c954d4446e5cb"},
]
