"""Regressões adicionais: ranking determinístico por valores exatos."""

from helpers import run_cli


def test_hotel_ranking_tiebreaks_by_hotel_id(tmp_path):
    """Hotéis com o mesmo total devem aparecer por ID ascendente."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H02", "hotel_name": "Hotel B", "amount": "100.00"},
            {"reservation_id": "R-2", "hotel_id": "H01", "hotel_name": "Hotel A", "amount": "100.00"},
            {"reservation_id": "R-3", "hotel_id": "H03", "hotel_name": "Hotel C", "amount": "90.00"},
        ],
        top=2,
    )
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H01", "H02"]
    assert len(report["top_hotels"]) == 2


def test_hotel_ranking_uses_exact_amount_before_money_rounding(tmp_path):
    """Dois valores exibidos como R$ 100,00 têm ordem definida pelos valores exatos."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H01", "hotel_name": "Hotel A", "amount": "100.001"},
            {"reservation_id": "R-2", "hotel_id": "H02", "hotel_name": "Hotel B", "amount": "100.004"},
            {"reservation_id": "R-3", "hotel_id": "H03", "hotel_name": "Hotel C", "amount": "99.50"},
        ],
        top=2,
    )
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H02", "H01"]
    assert [hotel["total_brl"] for hotel in report["top_hotels"]] == ["100.00", "100.00"]
