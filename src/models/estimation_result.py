# src/models/estimation_result.py

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class EstimationResult:

    id: int | None = None

    # Nouveau
    estimation_nom: str = ""

    # Contexte
    project_nom: str = ""
    profile_nom: str = ""
    scenario_nom: str = ""

    # Résultats calculés
    estimated_hours: float = 0.0
    estimated_days: float = 0.0
    estimated_cost: float = 0.0

    # Risque
    risk_factor: float = 1.0

    # Historique
    created_at: str = ""

    @classmethod
    def create(
        cls,
        project_nom: str,
        profile_nom: str,
        scenario_nom: str,
        estimated_hours: float,
        estimated_days: float,
        estimated_cost: float,
        risk_factor: float,
    ):

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        estimation_nom = f"{project_nom}_{scenario_nom}_{now[:10]}"

        return cls(
            estimation_nom=estimation_nom,
            project_nom=project_nom,
            profile_nom=profile_nom,
            scenario_nom=scenario_nom,
            estimated_hours=estimated_hours,
            estimated_days=estimated_days,
            estimated_cost=estimated_cost,
            risk_factor=risk_factor,
            created_at=now,
        )
