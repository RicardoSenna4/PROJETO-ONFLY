"""Regressões adicionais: conversão e precisão monetária."""

from decimal import Decimal

from helpers import run_cli
from onfly_report.services.currency_converter import convert_to_brl


def test_conversion_uses_exact_decimal_arithmetic():
    """O câmbio não deve perder centavos ao passar por float."""
    amount = Decimal("9007199254740993.01")
    rates = {"USD": Decimal("5.420000")}
    assert convert_to_brl(amount, "USD", rates) == amount * rates["USD"]


def test_conversion_multiplies_usd_and_eur_rates():
    """Valores são sempre convertidos por multiplicação com rate_to_brl."""
    rates = {"BRL": Decimal("1.000000"), "USD": Decimal("5.420000"), "EUR": Decimal("5.880000")}
    assert convert_to_brl(Decimal("0.10"), "BRL", rates) == Decimal("0.10")
    assert convert_to_brl(Decimal("0.10"), "USD", rates) == Decimal("0.54200000")
    assert convert_to_brl(Decimal("0.10"), "EUR", rates) == Decimal("0.58800000")


def test_rounding_only_after_sum_and_half_up_on_output(tmp_path):
    """Somar duas reservas de R$ 0,005 deve produzir R$ 0,01, não R$ 0,02."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "amount": "0.005"},
            {"reservation_id": "R-2", "amount": "0.005"},
        ],
    )
    assert report["summary"]["total_amount_brl"] == "0.01"
    assert report["by_month"][0]["total_brl"] == "0.01"
    assert report["top_hotels"][0]["total_brl"] == "0.01"


def test_half_up_on_single_fractional_cent(tmp_path):
    report = run_cli(tmp_path, [{"amount": "0.005"}])
    assert report["summary"]["total_amount_brl"] == "0.01"


def test_currency_precision_on_cli_with_usd_and_eur(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "currency": "USD", "amount": "1.005"},
            {"reservation_id": "R-2", "currency": "EUR", "amount": "2.005"},
        ],
    )
    # 1.005 * 5.42 + 2.005 * 5.88 = 17.2365, arredondado no JSON.
    assert report["summary"]["total_amount_brl"] == "17.24"
    assert report["summary"]["average_nightly_rate_brl"] == "8.62"
