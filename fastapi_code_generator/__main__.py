from fastapi_code_generator.cli import app, generate_code, invoke_main, main

__all__ = ["app", "generate_code", "invoke_main", "main"]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(invoke_main())
