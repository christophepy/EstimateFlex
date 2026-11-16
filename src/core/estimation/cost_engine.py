"""
EstimateFlex
Cost Engine

Calcule le coût estimé d'un projet à partir :
- des heures estimées
- du taux journalier
- du facteur de risque
"""

from dataclasses import dataclass

DEFAULT_HOURS_PER_DAY = 7.0


@dataclass(slots=True)
class CostBreakdown:
    """
    Détail des calculs de coût.
    """

    estimated_hours: float
    estimated_days: float
    daily_rate: float

    base_cost: float
    risk_factor: float

    final_cost: float


class CostEngine:
    """
    Moteur de calcul du coût projet.
    """

    HOURS_PER_DAY = DEFAULT_HOURS_PER_DAY

    @classmethod
    def calculate(
        cls,
        estimated_hours: float,
        daily_rate: float,
        risk_factor: float = 1.0,
        hours_per_day: float | None = None,
    ) -> CostBreakdown:
        """
        Calcul principal.

        Args:
            estimated_hours: charge estimée en heures
            daily_rate: TJM utilisateur
            risk_factor: multiplicateur de risque
            hours_per_day: nombre d'heures par jour

        Returns:
            CostBreakdown
        """

        estimated_hours = max(0.0, float(estimated_hours))
        daily_rate = max(0.0, float(daily_rate))
        risk_factor = max(1.0, float(risk_factor))

        hours_per_day = (
            float(hours_per_day) if hours_per_day is not None else cls.HOURS_PER_DAY
        )

        estimated_days = estimated_hours / hours_per_day

        base_cost = estimated_days * daily_rate

        final_cost = base_cost * risk_factor

        return CostBreakdown(
            estimated_hours=round(estimated_hours, 2),
            estimated_days=round(estimated_days, 2),
            daily_rate=round(daily_rate, 2),
            base_cost=round(base_cost, 2),
            risk_factor=round(risk_factor, 2),
            final_cost=round(final_cost, 2),
        )

    @classmethod
    def from_days(
        cls,
        estimated_days: float,
        daily_rate: float,
        risk_factor: float = 1.0,
        hours_per_day: float | None = None,
    ) -> CostBreakdown:
        """
        Calcul à partir d'un nombre de jours.
        """

        estimated_days = max(0.0, float(estimated_days))

        hours_per_day = (
            float(hours_per_day) if hours_per_day is not None else cls.HOURS_PER_DAY
        )

        return cls.calculate(
            estimated_hours=estimated_days * hours_per_day,
            daily_rate=daily_rate,
            risk_factor=risk_factor,
            hours_per_day=hours_per_day,
        )

    @staticmethod
    def margin(
        selling_price: float,
        estimated_cost: float,
    ) -> float:
        """
        Marge brute.
        """

        selling_price = float(selling_price)
        estimated_cost = float(estimated_cost)

        return round(selling_price - estimated_cost, 2)

    @staticmethod
    def margin_rate(
        selling_price: float,
        estimated_cost: float,
    ) -> float:
        """
        Taux de marge (%).
        """

        if selling_price <= 0:
            return 0.0

        margin = selling_price - estimated_cost

        return round((margin / selling_price) * 100.0, 2)
