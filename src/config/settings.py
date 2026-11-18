from dataclasses import dataclass, field


@dataclass(slots=True)
class ApplicationSettings:
    currency: str = "EUR"

    export_directory: str = ""

    date_format: str = "dd/MM/yyyy"

    exchange_rates: dict[str, float] = field(
        default_factory=lambda: {
            "EUR": 1.0,
            "USD": 1.08,
            "CHF": 0.94,
            "GBP": 0.86,
        }
    )
