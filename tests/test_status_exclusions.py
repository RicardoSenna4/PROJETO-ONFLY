"""Regressões adicionais: reservas não faturáveis não entram nas agregações."""

from helpers import run_cli


def test_non_billable_reservations_stay_out_of_monthly_and_hotels(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "status": "CONFIRMED", "hotel_id": "H01", "hotel_name": "Hotel A", "amount": "100.00"},
            {"reservation_id": "R-2", "status": "CANCELLED", "hotel_id": "H02", "hotel_name": "Hotel B", "amount": "50.00", "checkin_date": "2025-02-10", "checkout_date": "2025-02-11"},
            {"reservation_id": "R-3", "status": "NO_SHOW", "hotel_id": "H03", "hotel_name": "Hotel C", "amount": "20.00", "checkin_date": "2025-03-10", "checkout_date": "2025-03-11"},
        ],
    )

    assert report["summary"]["total_reservations"] == 3
    assert report["summary"]["confirmed_reservations"] == 1
    assert report["summary"]["cancelled_reservations"] == 1
    assert report["summary"]["no_show_reservations"] == 1
    assert report["summary"]["total_amount_brl"] == "100.00"
    assert report["summary"]["total_room_nights"] == 1
    assert [m["month"] for m in report["by_month"]] == ["2025-01"]
    assert report["by_month"][0]["reservations"] == 1
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H01"]
