# estimation_service.py

from datetime import datetime

from src.core.estimation.estimator import Estimator
from src.models.estimation_result import EstimationResult
from src.models.project import Project
from src.models.scenario import Scenario
from src.models.user_profile import UserProfile
from src.persistence.estimation_repository import (
    EstimationRepository,
)


class EstimationService:

    def __init__(
        self,
        repository: EstimationRepository | None = None,
    ):
        self.repository = repository or EstimationRepository()

        self.estimator = Estimator()

    def estimate(
        self,
        project: Project,
        profile: UserProfile,
        scenario: Scenario,
    ) -> EstimationResult:

        result = self.estimator.estimate(
            project=project,
            profile=profile,
        )

        result.scenario_nom = scenario.nom

        result.estimated_hours *= scenario.facteur_risque

        result.estimated_days *= scenario.facteur_risque

        result.estimated_cost *= scenario.facteur_risque

        result.estimated_days /= max(
            0.1,
            scenario.facteur_productivite,
        )

        result.estimated_days /= max(
            0.1,
            scenario.facteur_disponibilite,
        )

        result.estimated_hours = round(
            result.estimated_hours,
            2,
        )

        result.estimated_days = round(
            result.estimated_days,
            2,
        )

        result.estimated_cost = round(
            result.estimated_cost,
            2,
        )

        # ==================================================
        # Nom estimation
        # ==================================================

        result.estimation_nom = f"{project.nom}_" f"{scenario.nom}_V01"

        result.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ==================================================
        # Sauvegarde historique existante
        # ==================================================

        self.repository.save(result)

        return result
