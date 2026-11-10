# duration_engine.py
"""
EstimateFlex
Duration Engine

Calcul de la durée prévisionnelle d'un projet.
"""

from dataclasses import dataclass

DEFAULT_HOURS_PER_DAY = 7.0


@dataclass(slots=True)
class DurationBreakdown:
    """
    Résultat détaillé du calcul de durée.
    """

    estimated_hours: float

    productivity_factor: float
    risk_factor: float
    availability_factor: float

    adjusted_hours: float
    estimated_days: float


class DurationEngine:
    """
    Moteur de calcul de durée.
    """

    HOURS_PER_DAY = DEFAULT_HOURS_PER_DAY

    @classmethod
    def calculate(
        cls,
        estimated_hours: float,
        productivity_factor: float = 1.0,
        risk_factor: float = 1.0,
        availability_factor: float = 1.0,
    ) -> DurationBreakdown:
        """
        Calcule une durée à partir d'une charge estimée.

        Args:
            estimated_hours:
                Charge brute calculée par l'estimateur.

            productivity_factor:
                Productivité utilisateur.
                > 1.0 = plus rapide
                < 1.0 = plus lent

            risk_factor:
                Impact des risques.
                > 1.0 augmente la durée.

            availability_factor:
                Disponibilité réelle.
                Exemple :
                1.0 = 100%
                0.8 = 80%

        Returns:
            DurationBreakdown
        """

        estimated_hours = max(0.0, float(estimated_hours))

        productivity_factor = max(0.1, float(productivity_factor))
        risk_factor = max(1.0, float(risk_factor))
        availability_factor = max(0.1, float(availability_factor))

        # Plus la productivité est élevée,
        # moins il faut d'heures réelles.

        adjusted_hours = estimated_hours / productivity_factor

        adjusted_hours *= risk_factor

        adjusted_hours /= availability_factor

        estimated_days = adjusted_hours / cls.HOURS_PER_DAY

        return DurationBreakdown(
            estimated_hours=round(estimated_hours, 2),
            productivity_factor=round(productivity_factor, 2),
            risk_factor=round(risk_factor, 2),
            availability_factor=round(availability_factor, 2),
            adjusted_hours=round(adjusted_hours, 2),
            estimated_days=round(estimated_days, 2),
        )

    @classmethod
    def hours_to_days(
        cls,
        hours: float,
    ) -> float:
        """
        Convertit des heures en jours.
        """

        return round(
            max(0.0, float(hours)) / cls.HOURS_PER_DAY,
            2,
        )

    @classmethod
    def days_to_hours(
        cls,
        days: float,
    ) -> float:
        """
        Convertit des jours en heures.
        """

        return round(
            max(0.0, float(days)) * cls.HOURS_PER_DAY,
            2,
        )

    @staticmethod
    def working_weeks(
        estimated_days: float,
    ) -> float:
        """
        Conversion jours -> semaines.
        """

        return round(
            max(0.0, float(estimated_days)) / 5.0,
            2,
        )
