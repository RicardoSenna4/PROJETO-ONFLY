"""Teste end-to-end de regressão na exportação integral original."""

import json
from datetime import datetime, timedelta

from helpers import PROJECT_ROOT
from test_cli_contract_extended import invoke_cli


def test_complete_dataset_matches_independently_calculated_reference(tmp_path):
    report_path = tmp_path / "full.json"
    process = invoke_cli(
        "--input", PROJECT_ROOT / "data" / "reservas_hoteis.csv",
        "--rates", PROJECT_ROOT / "data" / "taxas_cambio.csv",
        "--output", report_path,
        "--top", "5",
    )
    assert process.returncode == 0, process.stderr
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["summary"] == {
        "total_reservations": 300,
        "confirmed_reservations": 235,
        "cancelled_reservations": 31,
        "no_show_reservations": 34,
        "total_room_nights": 1347,
        "total_amount_brl": "396170.00",
        "average_nightly_rate_brl": "294.11",
    }
    assert report["report_version"] == "1.0"
    assert datetime.fromisoformat(report["generated_at"]).utcoffset() == timedelta(hours=-3)
    months = [item["month"] for item in report["by_month"]]
    assert months == sorted(months)
    assert sum(row["reservations"] for row in report["by_month"]) == 235
    assert sum(row["room_nights"] for row in report["by_month"]) == 1347
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H06", "H10", "H12", "H07", "H11"]
