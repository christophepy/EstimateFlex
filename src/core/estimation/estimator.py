# Moteur principal d'estimation
# Coordonne tous les moteurs
# src/core/estimation/estimator.py

from src.core.estimation.cost_engine import (
    CostEngine,
)
from src.core.estimation.duration_engine import (
    DurationEngine,
)
from src.core.risk.risk_engine import (
    RiskEngine,
)
from src.models.estimation_result import (
    EstimationResult,
)
from src.models.project import Project
from src.models.user_profile import UserProfile


class Estimator:
    """
    Moteur principal d'estimation.
    """

    def __init__(self):

        self.cost_engine = CostEngine()
        self.duration_engine = DurationEngine()
        self.risk_engine = RiskEngine()

    def estimate(
        self,
        project: Project,
        profile: UserProfile,
    ) -> EstimationResult:
        """
        Retourne une estimation complète.
        """

        total_hours = self._calculate_hours(project)

        risk = self.risk_engine.calculate(
            planning_risk=2,
            scope_risk=2,
            technical_risk=2,
        )

        risk_factor = risk.factor

        adjusted_hours = total_hours * risk_factor

        duration = self.duration_engine.calculate(
            estimated_hours=adjusted_hours,
            productivity_factor=profile.facteur_productivite,
        )

        cost = self.cost_engine.calculate(
            estimated_hours=adjusted_hours,
            daily_rate=profile.taux_journalier,
            risk_factor=risk_factor,
        )

        return EstimationResult(
            project_nom=project.nom,
            profile_nom=profile.nom,
            estimated_hours=round(
                adjusted_hours,
                2,
            ),
            estimated_days=round(
                duration.estimated_days,
                2,
            ),
            estimated_cost=round(
                cost.final_cost,
                2,
            ),
            risk_factor=round(
                risk_factor,
                2,
            ),
        )

    def _calculate_hours(
        self,
        project: Project,
    ) -> float:

        p = project.parameters
        d = project.deliverables
        r = project.reviews

        total = 0.0

        # =====================================================
        # MODÉLISATION
        # =====================================================

        total += p.nb_lignes * 0.40

        total += p.nb_supports * 0.15

        total += p.nb_vannes * 0.08

        total += p.nb_brides * 0.04

        total += p.nb_compensateur * 0.50

        total += p.nb_connexions_equipements * 0.30

        # =====================================================
        # LIVRABLES CALCUL
        # =====================================================

        total += d.rapport_calcul * 16

        total += d.rapport_calcul_intermediare * 8

        total += d.fichier_resultat * 2

        # =====================================================
        # LIVRABLES PLANS
        # =====================================================

        total += d.notes_supports * 4

        total += d.notes_equipements * 4

        total += d.plans_supports * 6

        total += d.presentation_client * 4

        total += d.fichier_modele * 2

        # =====================================================
        # REVUES
        # =====================================================

        total += r.nb_revues_internes * 2

        total += r.nb_revues_client * 4

        total += r.nb_aller_retour * 3

        return round(
            total,
            2,
        )
