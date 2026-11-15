"""Testes complementares da interface CLI e de seus códigos de saída."""

import os
import subprocess
import sys

import pytest

from helpers import PROJECT_ROOT, SRC_DIR


def invoke_cli(*args):
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(SRC_DIR) + os.pathsep + environment.get("PYTHONPATH", "")
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-m", "onfly_report", *map(str, args)],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_cli_missing_required_arguments_returns_code_two():
    result = invoke_cli()
    assert result.returncode == 2
    assert "--input" in result.stderr


@pytest.mark.parametrize("top", [0, -1])
def test_cli_rejects_nonpositive_top_with_code_two(tmp_path, top):
    result = invoke_cli(
        "--input", PROJECT_ROOT / "data" / "exemplo-validacao.csv",
        "--rates", PROJECT_ROOT / "data" / "taxas_cambio.csv",
        "--output", tmp_path / "report.json", "--top", str(top),
    )
    assert result.returncode == 2
    assert "--top" in result.stderr
    assert not (tmp_path / "report.json").exists()


def test_cli_missing_reservations_file_returns_code_two(tmp_path):
    result = invoke_cli(
        "--input", tmp_path / "inexistente.csv",
        "--rates", PROJECT_ROOT / "data" / "taxas_cambio.csv",
        "--output", tmp_path / "report.json",
    )
    assert result.returncode == 2
    assert not (tmp_path / "report.json").exists()


def test_cli_missing_rates_file_returns_code_two(tmp_path):
    result = invoke_cli(
        "--input", PROJECT_ROOT / "data" / "exemplo-validacao.csv",
        "--rates", tmp_path / "sem_taxas.csv",
        "--output", tmp_path / "report.json",
    )
    assert result.returncode == 2
    assert not (tmp_path / "report.json").exists()


def test_cli_invalid_csv_header_returns_code_two(tmp_path):
    invalid = tmp_path / "invalid.csv"
    invalid.write_text("reservation_id,amount\nR-1,100.00\n", encoding="utf-8")
    result = invoke_cli(
        "--input", invalid,
        "--rates", PROJECT_ROOT / "data" / "taxas_cambio.csv",
        "--output", tmp_path / "report.json",
    )
    assert result.returncode == 2
    assert not (tmp_path / "report.json").exists()


def test_cli_creates_missing_output_parent_directories(tmp_path):
    nested = tmp_path / "nested" / "more" / "report.json"
    result = invoke_cli(
        "--input", PROJECT_ROOT / "data" / "exemplo-validacao.csv",
        "--rates", PROJECT_ROOT / "data" / "taxas_cambio.csv",
        "--output", nested,
    )
    assert result.returncode == 0, result.stderr
    assert nested.is_file()
    assert "Reservas: 12" in result.stdout


def test_cli_unexpected_output_io_failure_returns_code_one(tmp_path):
    parent_file = tmp_path / "not_a_directory"
    parent_file.write_text("already a file", encoding="utf-8")
    result = invoke_cli(
        "--input", PROJECT_ROOT / "data" / "exemplo-validacao.csv",
        "--rates", PROJECT_ROOT / "data" / "taxas_cambio.csv",
        "--output", parent_file / "report.json",
    )
    assert result.returncode == 1
