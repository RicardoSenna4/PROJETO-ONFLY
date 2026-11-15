"""Regressões adicionais: viradas de ano e mês e múltiplos quartos."""

from helpers import run_cli


def test_room_nights_across_year_with_multiple_rooms(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-YEAR",
                "checkin_date": "2025-12-30",
                "checkout_date": "2026-01-02",
                "rooms": "2",
            }
        ],
    )
    assert report["summary"]["total_room_nights"] == 6
    assert report["by_month"][0]["month"] == "2025-12"
    assert report["top_hotels"][0]["room_nights"] == 6


def test_room_nights_across_leap_day_with_multiple_rooms(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-LEAP",
                "checkin_date": "2024-02-28",
                "checkout_date": "2024-03-02",
                "rooms": "2",
            }
        ],
    )
    assert report["summary"]["total_room_nights"] == 6
