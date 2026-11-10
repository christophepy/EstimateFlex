from src.core.estimation.estimator import (
    Estimator,
)
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
from src.models.user_profile import (
    UserProfile,
)


def build_project():

    return Project(
        nom="HPC",
        client="EDF",
        description="Projet test",
        parameters=ProjectParameters(
            nb_lignes=10,
            nb_supports=20,
            nb_vannes=5,
            nb_brides=10,
            nb_compensateur=2,
            nb_connexions_equipements=3,
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
            nb_revues_internes=2,
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


def test_estimator_creation():

    estimator = Estimator()

    assert estimator is not None


def test_calculate_hours():

    estimator = Estimator()

    project = build_project()

    total = estimator._calculate_hours(project)

    assert total > 0


def test_calculate_hours_return_float():

    estimator = Estimator()

    project = build_project()

    total = estimator._calculate_hours(project)

    assert isinstance(
        total,
        float,
    )


def test_estimate_returns_result():

    estimator = Estimator()

    project = build_project()

    profile = build_profile()

    result = estimator.estimate(
        project,
        profile,
    )

    assert result is not None


def test_estimate_project_name():

    estimator = Estimator()

    result = estimator.estimate(
        build_project(),
        build_profile(),
    )

    assert result.project_nom == "HPC"


def test_estimate_profile_name():

    estimator = Estimator()

    result = estimator.estimate(
        build_project(),
        build_profile(),
    )

    assert result.profile_nom == "Senior"


def test_estimate_hours_positive():

    estimator = Estimator()

    result = estimator.estimate(
        build_project(),
        build_profile(),
    )

    assert result.estimated_hours > 0


def test_estimate_days_positive():

    estimator = Estimator()

    result = estimator.estimate(
        build_project(),
        build_profile(),
    )

    assert result.estimated_days > 0


def test_estimate_cost_positive():

    estimator = Estimator()

    result = estimator.estimate(
        build_project(),
        build_profile(),
    )

    assert result.estimated_cost > 0


def test_estimate_risk_factor_positive():

    estimator = Estimator()

    result = estimator.estimate(
        build_project(),
        build_profile(),
    )

    assert result.risk_factor > 0
