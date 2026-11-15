"""Regressões para a leitura integral da exportação de reservas."""

from pathlib import Path

from helpers import PROJECT_ROOT, run_cli

from onfly_report.repositories.csv_reservation_repository import CsvReservationRepository


def test_cli_processes_every_record_after_the_200th(tmp_path: Path) -> None:
    """Uma exportação válida com 205 linhas nunca deve perder as cinco finais."""
    rows = [
        {"reservation_id": f"R-{i:03d}", "amount": "1.00"}
        for i in range(1, 206)
    ]
    report = run_cli(tmp_path, rows)

    assert report["summary"]["total_reservations"] == 205
    assert report["summary"]["confirmed_reservations"] == 205
    assert report["summary"]["total_room_nights"] == 205
    assert report["summary"]["total_amount_brl"] == "205.00"
    assert report["by_month"][0]["reservations"] == 205
    assert report["top_hotels"][0]["room_nights"] == 205


def test_repository_reads_all_original_300_rows_in_order() -> None:
    """O repositório não deve interromper prematuramente a leitura do CSV original."""
    path = PROJECT_ROOT / "data" / "reservas_hoteis.csv"
    rows = CsvReservationRepository(path).read()

    assert len(rows) == 300
    assert len({row.values["reservation_id"] for row in rows}) == 300
    assert rows[0].line_number == 2
    assert rows[-1].line_number == 301
