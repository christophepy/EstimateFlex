from src.models.deliverables import (
    Deliverables,
)
from src.models.project import Project
from src.models.project_parameters import (
    ProjectParameters,
)
from src.models.review_metrics import (
    ReviewMetrics,
)
from src.models.scenario import (
    Scenario,
)
from src.models.user_profile import (
    UserProfile,
)
from src.services.estimation_service import (
    EstimationService,
)


class FakeRepository:

    def save(
        self,
        estimation,
    ):
        return None


def build_project():

    return Project(
        nom="HPC",
        client="EDF",
        description="Projet test",
        parameters=ProjectParameters(
            nb_lignes=10,
            nb_supports=5,
            nb_vannes=2,
            nb_brides=4,
            nb_compensateur=1,
            nb_connexions_equipements=2,
        ),
        deliverables=Deliverables(
            rapport_calcul=1,
            rapport_calcul_intermediare=1,
            fichier_resultat=1,
            notes_supports=1,
            notes_equipements=1,
            plans_supports=1,
            presentation_client=1,
            fichier_modele=1,
        ),
        reviews=ReviewMetrics(
            nb_revues_internes=1,
            nb_revues_client=1,
            nb_aller_retour=1,
        ),
    )


def build_profile():

    return UserProfile(
        nom="Senior",
        description="Profil test",
        taux_journalier=700,
        heures_par_jour=7,
        facteur_productivite=1.0,
    )


def build_scenario():

    return Scenario(
        nom="Réaliste",
        description="Scénario test",
        facteur_productivite=1.0,
        facteur_risque=1.0,
        facteur_disponibilite=1.0,
        actif=True,
    )


def build_service():

    return EstimationService(
        repository=FakeRepository(),
    )


def test_service_creation():

    service = build_service()

    assert service is not None


def test_estimate_returns_result():

    service = build_service()

    result = service.estimate(
        build_project(),
        build_profile(),
        build_scenario(),
    )

    assert result is not None


def test_estimation_name():

    service = build_service()

    result = service.estimate(
        build_project(),
        build_profile(),
        build_scenario(),
    )

    assert result.estimation_nom == "HPC_Réaliste_V01"


def test_project_name():

    service = build_service()

    result = service.estimate(
        build_project(),
        build_profile(),
        build_scenario(),
    )

    assert result.project_nom == "HPC"


def test_profile_name():

    service = build_service()

    result = service.estimate(
        build_project(),
        build_profile(),
        build_scenario(),
    )

    assert result.profile_nom == "Senior"


def test_scenario_name():

    service = build_service()

    result = service.estimate(
        build_project(),
        build_profile(),
        build_scenario(),
    )

    assert result.scenario_nom == "Réaliste"


def test_hours_positive():

    service = build_service()

    result = service.estimate(
        build_project(),
        build_profile(),
        build_scenario(),
    )

    assert result.estimated_hours > 0


def test_days_positive():

    service = build_service()

    result = service.estimate(
        build_project(),
        build_profile(),
        build_scenario(),
    )

    assert result.estimated_days > 0


def test_cost_positive():

    service = build_service()

    result = service.estimate(
        build_project(),
        build_profile(),
        build_scenario(),
    )

    assert result.estimated_cost > 0


def test_created_at_exists():

    service = build_service()

    result = service.estimate(
        build_project(),
        build_profile(),
        build_scenario(),
    )

    assert result.created_at != ""
