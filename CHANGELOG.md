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

## What's Changed
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

## New Contributors
* @marcoemorais made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/483
* @tobias-bahls made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/497
* @relaxbox made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/498
* @LuisHsu made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/454
* @greg80303 made their first contribution in https://github.com/koxudaxi/fastapi-code-generator/pull/493

**Full Changelog**: https://github.com/koxudaxi/fastapi-code-generator/compare/0.5.4...0.6.0

---
