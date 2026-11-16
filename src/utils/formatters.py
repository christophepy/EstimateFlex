# src/utils/formatters.py


def format_number(
    value: float,
    decimals: int = 2,
) -> str:
    """
    Format européen :
    12345.67 -> 12 345,67
    """

    return f"{value:,.{decimals}f}".replace(",", " ").replace(".", ",")


def format_currency(
    value: float,
    currency: str,
    decimals: int = 2,
) -> str:
    return f"{format_number(value, decimals)} " f"{currency}"
