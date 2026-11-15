"""Cobertura adicional do contrato de agregação e serialização JSON."""

import re
from datetime import datetime, timedelta

from helpers import run_cli


def test_no_confirmed_reservations_return_zero_values_and_empty_groups(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "status": "CANCELLED", "amount": "987.00"},
            {"reservation_id": "R-2", "status": "NO_SHOW", "amount": "654.00"},
        ],
    )
    assert report["summary"] == {
        "total_reservations": 2,
        "confirmed_reservations": 0,
        "cancelled_reservations": 1,
        "no_show_reservations": 1,
        "total_room_nights": 0,
        "total_amount_brl": "0.00",
        "average_nightly_rate_brl": "0.00",
    }
    assert report["by_month"] == []
    assert report["top_hotels"] == []


def test_monthly_report_uses_checkin_month_and_chronological_order(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-MAR", "checkin_date": "2025-03-31", "checkout_date": "2025-04-02"},
            {"reservation_id": "R-JAN", "checkin_date": "2025-01-31", "checkout_date": "2025-02-02"},
            {"reservation_id": "R-FEB", "checkin_date": "2025-02-28", "checkout_date": "2025-03-01"},
        ],
    )
    assert [row["month"] for row in report["by_month"]] == ["2025-01", "2025-02", "2025-03"]
    assert [row["room_nights"] for row in report["by_month"]] == [2, 1, 2]
    assert [row["total_brl"] for row in report["by_month"]] == ["100.00"] * 3
    assert report["summary"]["total_room_nights"] == 5


def test_quoted_comma_in_hotel_name_is_preserved(tmp_path):
    report = run_cli(
        tmp_path,
        [{"hotel_id": "H42", "hotel_name": "Hotel Madrid, Gran Vía", "amount": "12.50"}],
    )
    assert report["top_hotels"][0]["hotel_id"] == "H42"
    assert report["top_hotels"][0]["hotel_name"] == "Hotel Madrid, Gran Vía"
    assert report["summary"]["total_amount_brl"] == "12.50"


def test_json_schema_types_two_decimal_places_and_fixed_timezone(tmp_path):
    report = run_cli(tmp_path, [{"reservation_id": "R-SCHEMA", "amount": "12.345"}])
    assert set(report) == {"report_version", "generated_at", "summary", "by_month", "top_hotels"}
    assert report["report_version"] == "1.0"
    assert datetime.fromisoformat(report["generated_at"]).utcoffset() == timedelta(hours=-3)
    summary = report["summary"]
    assert set(summary) == {
        "total_reservations", "confirmed_reservations", "cancelled_reservations",
        "no_show_reservations", "total_room_nights", "total_amount_brl", "average_nightly_rate_brl",
    }
    for key in ("total_reservations", "confirmed_reservations", "cancelled_reservations",
                "no_show_reservations", "total_room_nights"):
        assert type(summary[key]) is int
    assert set(report["by_month"][0]) == {"month", "reservations", "room_nights", "total_brl"}
    assert set(report["top_hotels"][0]) == {"hotel_id", "hotel_name", "room_nights", "total_brl"}
    assert type(report["by_month"][0]["reservations"]) is int
    assert type(report["by_month"][0]["room_nights"]) is int
    assert type(report["top_hotels"][0]["room_nights"]) is int
    for amount in (summary["total_amount_brl"], summary["average_nightly_rate_brl"],
                   report["by_month"][0]["total_brl"], report["top_hotels"][0]["total_brl"]):
        assert isinstance(amount, str)
        assert re.fullmatch(r"-?\d+\.\d{2}", amount)
    assert summary["total_amount_brl"] == "12.35"


def test_top_one_limits_list_to_highest_hotel(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H01", "hotel_name": "Menor", "amount": "100.00"},
            {"reservation_id": "R-2", "hotel_id": "H02", "hotel_name": "Maior", "amount": "200.00"},
        ],
        top=1,
    )
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H02"]


def test_more_requested_hotels_than_exist_returns_only_existing(tmp_path):
    report = run_cli(tmp_path, [{"hotel_id": "H01", "hotel_name": "Único"}], top=50)
    assert len(report["top_hotels"]) == 1
    assert report["top_hotels"][0]["hotel_name"] == "Único"


def test_status_counts_include_records_after_line_200(tmp_path):
    rows = [{"reservation_id": f"R-{i:03d}", "amount": "1.00"} for i in range(1, 204)]
    rows.extend([
        {"reservation_id": "R-204", "status": "CANCELLED", "amount": "10000.00"},
        {"reservation_id": "R-205", "status": "NO_SHOW", "amount": "10000.00"},
    ])
    report = run_cli(tmp_path, rows)
    summary = report["summary"]
    assert summary["total_reservations"] == 205
    assert summary["confirmed_reservations"] == 203
    assert summary["cancelled_reservations"] == 1
    assert summary["no_show_reservations"] == 1
    assert summary["total_room_nights"] == 203
    assert summary["total_amount_brl"] == "203.00"
