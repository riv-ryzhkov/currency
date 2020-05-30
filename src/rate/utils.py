from decimal import Decimal


def to_decimal(value, prec: int = 2) -> Decimal:
    return round(Decimal(value), prec)