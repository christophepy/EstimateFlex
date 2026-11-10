# Calcul de la réserve de risque
# src/core/risk/risk_engine.py

from dataclasses import dataclass


@dataclass
class RiskResult:
    score: float
    factor: float


class RiskEngine:

    @staticmethod
    def calculate(
        planning_risk: int, scope_risk: int, technical_risk: int
    ) -> RiskResult:

        score = (planning_risk + scope_risk + technical_risk) / 3

        factor = 1 + (score * 0.10)

        return RiskResult(score=round(score, 2), factor=round(factor, 2))
