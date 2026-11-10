# Calcul des scénarios
"""
EstimateFlex
Scenario Engine
"""

from dataclasses import dataclass
from enum import StrEnum


class ScenarioType(StrEnum):
    OPTIMISTIC = "Optimistic"
    REALISTIC = "Realistic"
    PESSIMISTIC = "Pessimistic"


@dataclass(slots=True)
class ScenarioResult:
    """
    Résultat d'un scénario.
    """

    scenario: str

    estimated_hours: float
    estimated_days: float
    estimated_cost: float

    effort_multiplier: float
    risk_multiplier: float


class ScenarioEngine:
    """
    Générateur de scénarios.
    """

    SCENARIOS = {
        ScenarioType.OPTIMISTIC: {
            "effort_multiplier": 0.85,
            "risk_multiplier": 0.95,
        },
        ScenarioType.REALISTIC: {
            "effort_multiplier": 1.00,
            "risk_multiplier": 1.00,
        },
        ScenarioType.PESSIMISTIC: {
            "effort_multiplier": 1.25,
            "risk_multiplier": 1.15,
        },
    }

    @classmethod
    def build(
        cls,
        base_hours: float,
        base_days: float,
        base_cost: float,
        scenario_type: ScenarioType,
    ) -> ScenarioResult:
        """
        Génération d'un scénario unique.
        """

        config = cls.SCENARIOS[scenario_type]

        effort_factor = config["effort_multiplier"]
        risk_factor = config["risk_multiplier"]

        estimated_hours = base_hours * effort_factor
        estimated_days = base_days * effort_factor
        estimated_cost = base_cost * effort_factor * risk_factor

        return ScenarioResult(
            scenario=scenario_type.value,
            estimated_hours=round(estimated_hours, 2),
            estimated_days=round(estimated_days, 2),
            estimated_cost=round(estimated_cost, 2),
            effort_multiplier=round(effort_factor, 2),
            risk_multiplier=round(risk_factor, 2),
        )

    @classmethod
    def generate_all(
        cls,
        base_hours: float,
        base_days: float,
        base_cost: float,
    ) -> list[ScenarioResult]:
        """
        Génère les trois scénarios standards.
        """

        return [
            cls.build(
                base_hours,
                base_days,
                base_cost,
                ScenarioType.OPTIMISTIC,
            ),
            cls.build(
                base_hours,
                base_days,
                base_cost,
                ScenarioType.REALISTIC,
            ),
            cls.build(
                base_hours,
                base_days,
                base_cost,
                ScenarioType.PESSIMISTIC,
            ),
        ]

    @staticmethod
    def best_case(scenarios: list[ScenarioResult]) -> ScenarioResult:
        """
        Retourne le scénario le plus favorable.
        """

        return min(
            scenarios,
            key=lambda s: s.estimated_cost,
        )

    @staticmethod
    def worst_case(scenarios: list[ScenarioResult]) -> ScenarioResult:
        """
        Retourne le scénario le plus défavorable.
        """

        return max(
            scenarios,
            key=lambda s: s.estimated_cost,
        )

    @staticmethod
    def average_cost(
        scenarios: list[ScenarioResult],
    ) -> float:
        """
        Coût moyen.
        """

        if not scenarios:
            return 0.0

        return round(
            sum(s.estimated_cost for s in scenarios) / len(scenarios),
            2,
        )
