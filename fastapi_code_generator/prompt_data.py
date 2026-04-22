"""Auto-generated prompt data from cli_doc collection.

DO NOT EDIT MANUALLY. Run: python scripts/build_prompt_data.py
"""

from __future__ import annotations

# Option descriptions extracted from cli_doc markers
OPTION_DESCRIPTIONS: dict[str, str] = {
    "--custom-visitor": "Load a custom visitor module and expose additional template variables.",
    "--disable-timestamp": "Omit the generated timestamp header from output files.",
    "--encoding": "Read the input schema using an explicit text encoding.",
    "--enum-field-as-literal": "Render enum fields as Literal annotations.",
    "--generate-routers": "Generate modular router files from tagged OpenAPI operations.",
    "--help": "Show the CLI help message.",
    "--input": "Generate a FastAPI application from an OpenAPI input file.",
    "--model-file": "Write generated models to a custom module path.",
    "--model-template-dir": "Use a custom datamodel-code-generator template directory.",
    "--output": "Directory where the generated FastAPI application is written.",
    "--output-model-type": "Choose the datamodel-code-generator output backend.",
    "--python-version": "Target a specific Python version when formatting generated code.",
    "--specify-tags": "Regenerate only the routers matching a comma-separated tag list.",
    "--template-dir": "Render generated files with a custom template directory.",
    "--version": "Show the installed fastapi-codegen version.",
}
