# main.py
from typing import Dict, List


def set_rate(rates: Dict[str, float], code: str, rate_to_base: float) -> None:
    if rate_to_base <= 0:
        raise ValueError("rate must be > 0")
    rates[code.upper()] = rate_to_base


def convert(rates: Dict[str, float], amount: float, from_code: str, to_code: str) -> float:
    if amount < 0:
        raise ValueError("amount must be >= 0")
    src = from_code.upper()
    dst = to_code.upper()
    if src not in rates or dst not in rates:
        raise KeyError("unknown currency")
    in_base = amount * rates[src]
    return in_base / rates[dst]


def list_currencies(rates: Dict[str, float]) -> List[str]:
    return sorted(rates.keys())


def has_currency(rates: Dict[str, float], code: str) -> bool:
    return code.upper() in rates
