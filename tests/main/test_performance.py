from __future__ import annotations

from pathlib import Path

import pytest

from tests.main.conftest import DATA_PATH, run_main_with_args


@pytest.mark.perf
@pytest.mark.benchmark
def test_generate_default_template_benchmark(
    benchmark: pytest.BenchmarkFixture, tmp_path: Path
) -> None:
    source = DATA_PATH / "openapi" / "default_template" / "simple.yaml"

    def run() -> None:
        output_dir = tmp_path / "generated"
        if output_dir.exists():
            for path in sorted(output_dir.rglob("*"), reverse=True):
                if path.is_file():
                    path.unlink()
                else:
                    path.rmdir()
            output_dir.rmdir()
        assert (
            run_main_with_args(
                [
                    "--input",
                    str(source),
                    "--output",
                    str(output_dir),
                ]
            )
            == 0
        )

    benchmark(run)
