import pytest
from main import set_rate, convert, list_currencies, has_currency


def test_set_rate_valid():
    rates = {}
    set_rate(rates, "usd", 1.0)
    set_rate(rates, "EUR", 1.1)
    assert rates == {"USD": 1.0, "EUR": 1.1}


def test_set_rate_invalid():
    rates = {}
    with pytest.raises(ValueError, match="rate must be > 0"):
        set_rate(rates, "USD", 0)
    with pytest.raises(ValueError, match="rate must be > 0"):
        set_rate(rates, "USD", -1.5)


def test_convert_success():
    rates = {"USD": 1.0, "EUR": 1.2, "BYN": 0.3}
    # 100 EUR = 120 base, 120 / 1.0 = 120 USD
    result = convert(rates, 100.0, "EUR", "USD")
    assert pytest.approx(result, 0.0001) == 120.0

    # 0 amount
    assert convert(rates, 0.0, "USD", "EUR") == 0.0

    # lowercase codes
    result_lower = convert(rates, 50.0, "byn", "usd")
    assert pytest.approx(result_lower, 0.0001) == 15.0


def test_convert_negative_amount():
    rates = {"USD": 1.0, "EUR": 1.2}
    with pytest.raises(ValueError, match="amount must be >= 0"):
        convert(rates, -10.0, "USD", "EUR")


def test_convert_unknown_currency():
    rates = {"USD": 1.0}
    with pytest.raises(KeyError, match="unknown currency"):
        convert(rates, 100.0, "USD", "GBP")
    with pytest.raises(KeyError, match="unknown currency"):
        convert(rates, 100.0, "JPY", "USD")


def test_list_currencies():
    rates = {"USD": 1.0, "BYN": 0.3, "EUR": 1.2}
    assert list_currencies(rates) == ["BYN", "EUR", "USD"]
    assert list_currencies({}) == []


def test_has_currency():
    rates = {"USD": 1.0, "EUR": 1.2}
    assert has_currency(rates, "usd") is True
    assert has_currency(rates, "USD") is True
    assert has_currency(rates, "eur") is True
    assert has_currency(rates, "RUB") is False
