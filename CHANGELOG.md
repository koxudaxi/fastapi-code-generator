# Changelog

All notable changes to this project are documented in this file.
This changelog is automatically generated from GitHub Releases.

---

## [0.6.0](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.6.0) - 2026-04-30

## Breaking Changes


### Python or Dependency Support Changes
* Dropped Python 3.9 runtime support - Package metadata now requires Python 3.10 or newer, removes the Python 3.9 classifier, and updates the supported runtime range to Python 3.10 through 3.14 (#514)
* Dropped Python 3.9 target generation - The CLI `--python-version` choices no longer include `3.9`, so users generating Python 3.9-compatible output need to stay on an older release or target Python 3.10+ (#534)

### API/CLI Changes
* Removed the Pydantic v1 BaseModel output option - `--output-model-type` no longer exposes `pydantic.BaseModel`, and scripts that pass that value need to switch to a supported output backend (#534)

### Default Behavior Changes
* Changed the default model backend to Pydantic v2 - `--output-model-type` now defaults to `pydantic_v2.BaseModel`, which changes generated model imports and configuration unless users explicitly choose another backend (#534)

### Code Generation Changes
* Changed generated FastAPI parameter and model output - Optional query parameters may now use explicit `Query(...)` defaults or aliases, and generated models move from Pydantic v1 patterns to Pydantic v2-style configuration (#534)

### What's Changed
* remove typed-ast (EOL) from dependencies and update poetry.lock by @marcoemorais in https://github.com/koxudaxi/fastapi-code-generator/pull/483
* Bump pytest-cov from 5.0.0 to 7.1.0 by @dependabot[bot] in https://github.com/koxudaxi/fastapi-code-generator/pull/502
* chore: migrate to uv and support Python 3.10-3.14 by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/514
* Add CLI E2E coverage pipeline by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/516
* Port workflow and docs automation stack by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/517
* Update hatchling requirement from >=1.27 to >=1.29.0 by @dependabot[bot] in https://github.com/koxudaxi/fastapi-code-generator/pull/528
* Align CI/CD hardening workflows by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/538
* Align CI workflows with datamodel-code-generator by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/539
* Harden generated docs CI checks by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/551
* Update datamodel-code-generator to 0.56.1 by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/534
* fix: Allow hyphen in tags by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/552
* fix: Allow hyphen in tags by @tobias-bahls in https://github.com/koxudaxi/fastapi-code-generator/pull/497
* Fix a versioning issue with click by @relaxbox in https://github.com/koxudaxi/fastapi-code-generator/pull/498
* Support for use-annotated by @jnu in https://github.com/koxudaxi/fastapi-code-generator/pull/518
* Fix PR 518 followups by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/555
* Preserve router path parameter names by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/554
* Expose plain arguments by @LuisHsu in https://github.com/koxudaxi/fastapi-code-generator/pull/454
* Fix multiple file upload generation by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/553
* Add support for setting strict_nullable from CLI by @greg80303 in https://github.com/koxudaxi/fastapi-code-generator/pull/493
* Fix specify-tags router filtering by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/558
* Fix stringcase dependency with setuptools 78.0.0 by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/565
* Add faux immutability option by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/569
* Fix discriminated union simple types by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/566
* Expose reuse model option by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/568
* Preserve query array parameter types by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/567
* Restore release draft analysis by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/571
* Fix release draft gh repository context by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/572
* Fix release draft label permissions by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/573
* Use REST API for release draft labels by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/574
* Fix release draft PR label scope by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/575

### New Contributors
* @marcoemorais made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/483
* @tobias-bahls made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/497
* @relaxbox made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/498
* @LuisHsu made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/454
* @greg80303 made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/493

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.5.4...0.6.0

---

## [0.5.4](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.5.4) - 2025-04-29

### What's Changed

* Remove deprecated datamodel-code-generator patch by @sternakt in https://github.com/koxudaxi/fastapi-code-generator/pull/489
* Bump version by @sternakt in https://github.com/koxudaxi/fastapi-code-generator/pull/490

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.5.3...0.5.4

---

## [0.5.3](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.5.3) - 2025-04-16

### What's Changed
* Improve code generation with fixes for recursion, aliasing, and modular references by @sternakt in https://github.com/koxudaxi/fastapi-code-generator/pull/484
* Fix docs build in CI by @davorrunje in https://github.com/koxudaxi/fastapi-code-generator/pull/485
* Fix publish in CI by @davorrunje in https://github.com/koxudaxi/fastapi-code-generator/pull/486

### New Contributors
* @sternakt made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/484

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.5.2...0.5.3

---

## [0.5.3rc0](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.5.3rc0) - 2025-04-16

### What's Changed
* Improve code generation with fixes for recursion, aliasing, and modular references by @sternakt in https://github.com/koxudaxi/fastapi-code-generator/pull/484
* Fix docs build in CI by @davorrunje in https://github.com/koxudaxi/fastapi-code-generator/pull/485
* Fix publish in CI by @davorrunje in https://github.com/koxudaxi/fastapi-code-generator/pull/486

### New Contributors
* @sternakt made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/484

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.5.2...0.5.3rc0

---

## [0.5.2](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.5.2) - 2024-12-14

### What's Changed
* Fix target_python_version by @chantera in https://github.com/koxudaxi/fastapi-code-generator/pull/445
* Fix parameter field name by @chantera in https://github.com/koxudaxi/fastapi-code-generator/pull/446
* Add `--model-template-dir` option by @chantera in https://github.com/koxudaxi/fastapi-code-generator/pull/447

### New Contributors
* @chantera made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/445

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.5.1...0.5.2

---

## [0.5.1](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.5.1) - 2024-07-02

### What's Changed
* Update typer by @davorrunje in https://github.com/koxudaxi/fastapi-code-generator/pull/430
* Support for Pydantic 2 & additional python versions by @jnu in https://github.com/koxudaxi/fastapi-code-generator/pull/414
* Fix generate_code args by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/436
* fix inconsistency routers<>tags arrays by @azdolinski in https://github.com/koxudaxi/fastapi-code-generator/pull/417
* 419 / Support for parsing callbacks by @jnu in https://github.com/koxudaxi/fastapi-code-generator/pull/420

### New Contributors
* @davorrunje made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/430
* @jnu made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/414
* @azdolinski made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/417

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.5.0...0.5.1

---

## [0.5.0](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.5.0) - 2024-05-02

### What's Changed
* Update pydantic to v2 and update datamodel-code-generator to 0.25.6 by @kumaranvpl in https://github.com/koxudaxi/fastapi-code-generator/pull/408

### New Contributors
* @kumaranvpl made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/408

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.4.4...0.5.0

---

## [0.4.4](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.4.4) - 2023-09-07

### What's Changed
* Generate correct python code if path is camel case by @yyamano in https://github.com/koxudaxi/fastapi-code-generator/pull/380
* Generate valid python code if query param exists and requestBody is required by @yyamano in https://github.com/koxudaxi/fastapi-code-generator/pull/382
* Allow modular output with custom templates by @notpushkin in https://github.com/koxudaxi/fastapi-code-generator/pull/384
* Fixed broken test (Added option for inputting encoding of file #334) by @yyamano in https://github.com/koxudaxi/fastapi-code-generator/pull/383

### New Contributors
* @notpushkin made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/384

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.4.3...0.4.4

---

## [0.4.3](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.4.3) - 2023-08-19

### What's Changed
* Don't overwrite files in tests/data at testing time by @yyamano in https://github.com/koxudaxi/fastapi-code-generator/pull/373
* Add file upload support for both octet-stream and form-data by @yyamano in https://github.com/koxudaxi/fastapi-code-generator/pull/374
* Generate valid python code if query param has default value and requestBody is required by @yyamano in https://github.com/koxudaxi/fastapi-code-generator/pull/377
* Generate an empty model file if an api spec file have no "schemas". by @yyamano in https://github.com/koxudaxi/fastapi-code-generator/pull/375

### New Contributors
* @yyamano made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/373

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.4.2...0.4.3

---

## [0.4.2](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.4.2) - 2023-04-27

### What's Changed
* Feature/generate routers by @v1kAn0v in https://github.com/koxudaxi/fastapi-code-generator/pull/344
* Enable custom visitors when enum_field_as_literal parameter is passed by @dmille in https://github.com/koxudaxi/fastapi-code-generator/pull/332

### New Contributors
* @v1kAn0v made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/344
* @dmille made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/332

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.4.1...0.4.2

---

## [0.4.1](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.4.1) - 2023-02-15

### What's Changed
* Add support for file upload (application/octet-stream) by @david-westreicher in https://github.com/koxudaxi/fastapi-code-generator/pull/313
* Add `--disable-timestamp` by @ytoml in https://github.com/koxudaxi/fastapi-code-generator/pull/324

### New Contributors
* @david-westreicher made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/313
* @ytoml made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/324

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.4.0...0.4.1

---

## [0.4.0](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.4.0) - 2023-01-17

### What's Changed
* add tags to default template by @n0nvme in https://github.com/koxudaxi/fastapi-code-generator/pull/309
* Update datamodel-code-generator by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/311

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.3.6...0.4.0

---

## [0.3.6](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.3.6) - 2022-10-24

### What's Changed
* Fix tests - Issue #260 by @jcarlosgalvezm in https://github.com/koxudaxi/fastapi-code-generator/pull/266
* add custom variables support by @sofianhnaide in https://github.com/koxudaxi/fastapi-code-generator/pull/247
* Bump jinja2 from 3.0.3 to 3.1.2 by @dependabot in https://github.com/koxudaxi/fastapi-code-generator/pull/250
* add .pre-commit-config.yaml by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/283
* Update dependencies by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/284

### New Contributors
* @jcarlosgalvezm made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/266
* @sofianhnaide made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/247

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.3.5...0.3.6

---

## [0.3.5](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.3.5) - 2022-05-13

### What's Changed
* Update datamodel code generator to 0.11.19 by @n0nvme in https://github.com/koxudaxi/fastapi-code-generator/pull/231

### New Contributors
* @n0nvme made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/231

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.3.4...0.3.5

---

## [0.3.4](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.3.4) - 2021-12-03

### What's Changed
* Adding support for datamodel-code-generator's enum-field-as-literal argument by @LongBeachHXC in https://github.com/koxudaxi/fastapi-code-generator/pull/224

### New Contributors
* @LongBeachHXC made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/224

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.3.3...0.3.4

---

## [0.3.3](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.3.3) - 2021-12-03

### What's Changed
* Fix model file by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/223


**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.3.2...0.3.3

---

## [0.3.2](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.3.2) - 2021-11-29

### What's Changed
* Fix unittest by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/219
* update datamodel-code-generator to 0.11.15 by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/220


**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.3.1...0.3.2

---

## [0.3.1](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.3.1) - 2021-11-28

### What's Changed
* Add description on operation by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/187
* Bump datamodel-code-generator from 0.11.9 to 0.11.11 by @dependabot in https://github.com/koxudaxi/fastapi-code-generator/pull/188
* Bump typer from 0.3.2 to 0.4.0 by @dependabot in https://github.com/koxudaxi/fastapi-code-generator/pull/193
* Bump pytest from 6.2.4 to 6.2.5 by @dependabot in https://github.com/koxudaxi/fastapi-code-generator/pull/194
* Update datamodel-code-generator to 0.11.12 by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/195
* Bump datamodel-code-generator from 0.11.12 to 0.11.13 by @dependabot in https://github.com/koxudaxi/fastapi-code-generator/pull/198
* Bump datamodel-code-generator from 0.11.13 to 0.11.14 by @dependabot in https://github.com/koxudaxi/fastapi-code-generator/pull/200
* Bump jinja2 from 3.0.1 to 3.0.3 by @dependabot in https://github.com/koxudaxi/fastapi-code-generator/pull/211
* Bump pytest-cov from 2.12.1 to 3.0.0 by @dependabot in https://github.com/koxudaxi/fastapi-code-generator/pull/202
* Fix typed-ast by @koxudaxi in https://github.com/koxudaxi/fastapi-code-generator/pull/216
* Add additional responses by @rominf in https://github.com/koxudaxi/fastapi-code-generator/pull/203
* Added option to specify model file instead of defaulting to models.py by @baophamtd in https://github.com/koxudaxi/fastapi-code-generator/pull/204
* Add servers by @rominf in https://github.com/koxudaxi/fastapi-code-generator/pull/206

### New Contributors
* @rominf made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/203
* @baophamtd made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/204

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.3.0...0.3.1

---

## [0.3.0](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.3.0) - 2021-08-08

- Refactor parser [#167]

---

## [0.2.7](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.2.7) - 2021-06-17

- Fix invalid argument order [#174]

---

## [0.2.6](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.2.6) - 2021-05-29

- Add the various parameter in operators for query, path, header, body [#162] by @allen-munsch

Thanks to @allen-munsch

---

## [0.2.5](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.2.5) - 2021-05-04

- Update datamodel-code-generator to 0.11.3 [#150]
- Support content in parameters [#149]

---

## [0.2.4](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.2.4) - 2021-04-29

- now it's possible to use tags in templates [#144] by @yetanotherjsontodatabaseexporter

Thanks to @yetanotherjsontodatabaseexporter

---

## [0.2.3](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.2.3) - 2021-03-01

- Support form with Request [#121]

---

## [0.2.2](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.2.2) - 2021-02-19

Add model module name [#113]

---

## [0.2.1](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.2.1) - 2021-02-18

- Update datamodel-code-generator to 0.8.1 [#112]

---

## [0.2.0](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.2.0) - 2021-01-25

- Support embedded array schema [#100]
- Support embedded schema [#99]
- Update datamodel-code-generator to 0.6.22 [#91]

---

## [0.1.1](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.1.1) - 2021-01-12

- Fix resolving template path [#87]

---

## [0.1.0](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.1.0) - 2021-01-07

- update datamodel-code-generator to 0.6.17 [#83]
- Support multi-line string values for openapi keys [#80] by @ bpow

Thanks to @bpow

---

## [0.0.19](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.19) - 2020-12-02

- move black to dev dependencies [#65]

---

## [0.0.18](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.18) - 2020-11-21

- support summary [#63]

---

## [0.0.17](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.17) - 2020-11-14

- Support python39 [#59]
- Support python37 [#58]
- Support remote ref on parameters, requestBodies and responses [#57]
- Use re.compiled object [#50] by @ioggstream

Thanks to @ioggstream

---

## [0.0.16](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.16) - 2020-11-10

- support $ref parameter [#49]

---

## [0.0.15](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.15) - 2020-11-09

- support application json variant [#47 ]

---

## [0.0.14](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.14) - 2020-11-04

- improve model management [#45]
- add info parser [#42] by @akuma5157
- support $ref in response [#29]

Thanks to @akuma5157

---

## [0.0.13](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.13) - 2020-07-27

- Yaml is a superset of json. [#23]  by @ioggstream

Thanks to @ioggstream

---

## [0.0.12](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.12) - 2020-06-26

- Support security [#22]

---

## [0.0.11](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.11) - 2020-06-20

- fix invalid query parameter [#21]

---

## [0.0.10](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.10) - 2020-06-20

- fix default [#20]

---

## [0.0.9](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.9) - 2020-06-19

- fix default value of query parameter [#18]

---

## [0.0.8](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.8) - 2020-06-18

- fix invalid required [#14]

---

## [0.0.7](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.7) - 2020-06-18

- Support aliased query parameter [#11]

---

## [0.0.6](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.6) - 2020-06-17

- add fields to argument [#10]

---

## [0.0.5](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.5) - 2020-06-17

- fix default arguments [#9]

---

## [0.0.4](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.4) - 2020-06-16

- fix invalid root_path and parameters [#8]

---

## [0.0.3](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.3) - 2020-06-16

- refactor parse paths method [#5]

---

## [0.0.2](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.2) - 2020-06-15

- Refactor openapi parser [#4]

---

## [0.0.1](https://github.com/koxudaxi/fastapi-code-generator/releases/tag/0.0.1) - 2020-06-14

- support to generate simple main.py

---
