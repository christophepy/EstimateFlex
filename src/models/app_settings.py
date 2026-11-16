from dataclasses import dataclass, field

DEFAULT_EXCHANGE_RATES = {
    "EUR": 1.0,
    "USD": 1.08,
    "CHF": 0.94,
    "GBP": 0.86,
}


@dataclass(slots=True)
class AppSettings:

    currency: str = "EUR"

    exchange_rates: dict[str, float] = field(
        default_factory=lambda: DEFAULT_EXCHANGE_RATES.copy()
    )

    export_directory: str = "exports"

    theme: str = "light"

    font_size: int = 10

    show_dashboard_kpis: bool = True
    show_dashboard_charts: bool = True

    def to_dict(self) -> dict:
        """Conversion vers dictionnaire JSON."""
        return {
            "currency": self.currency,
            "exchange_rates": self.exchange_rates,
            "export_directory": self.export_directory,
            "theme": self.theme,
            "font_size": self.font_size,
            "show_dashboard_kpis": self.show_dashboard_kpis,
            "show_dashboard_charts": self.show_dashboard_charts,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AppSettings":
        """Création depuis un dictionnaire JSON."""
        return cls(
            currency=data.get("currency", "EUR"),
            exchange_rates=dict(
                data.get(
                    "exchange_rates",
                    DEFAULT_EXCHANGE_RATES,
                )
            ),
            export_directory=data.get(
                "export_directory",
                "exports",
            ),
            theme=data.get(
                "theme",
                "light",
            ),
            font_size=int(
                data.get(
                    "font_size",
                    10,
                )
            ),
            show_dashboard_kpis=bool(
                data.get(
                    "show_dashboard_kpis",
                    True,
                )
            ),
            show_dashboard_charts=bool(
                data.get(
                    "show_dashboard_charts",
                    True,
                )
            ),
        )
