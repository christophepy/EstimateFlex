from src.core.formulas.formulas import (
    calcul_cout,
    calcul_cout_total,
    calcul_effort_total,
    calcul_estimation,
    calcul_taux_horaire,
    effort_brides,
    effort_equipements,
    effort_lignes,
    effort_supports,
    effort_vannes,
)
from src.models.deliverables import (
    Deliverables,
)
from src.models.project_parameters import (
    ProjectParameters,
)
from src.models.review_metrics import (
    ReviewMetrics,
)
from src.models.user_profile import (
    UserProfile,
)


def build_profile():

    profile = UserProfile(
        nom="Senior",
        description="Test",
    )

    profile.taux_journalier = 700
    profile.heures_par_jour = 7

    profile.heure_par_ligne = 1.0
    profile.heure_par_support = 0.5
    profile.heure_par_vanne = 0.25
    profile.heure_par_bride = 0.10
    profile.heure_par_equipement = 0.20

    profile.heure_par_note_de_calcul = 2.0
    profile.heure_par_presentation = 3.0
    profile.heure_par_verification = 1.0

    return profile


def test_effort_lignes():

    assert (
        effort_lignes(
            10,
            0.5,
        )
        == 5.0
    )


def test_effort_supports():

    assert (
        effort_supports(
            10,
            0.2,
        )
        == 2.0
    )


def test_effort_vannes():

    assert (
        effort_vannes(
            4,
            0.5,
        )
        == 2.0
    )


def test_effort_brides():

    assert (
        effort_brides(
            20,
            0.1,
        )
        == 2.0
    )


def test_effort_equipements():

    assert (
        effort_equipements(
            5,
            0.4,
        )
        == 2.0
    )


def test_calcul_effort_total():

    assert (
        calcul_effort_total(
            10,
            5,
            2,
        )
        == 17
    )


def test_taux_horaire():

    profile = build_profile()

    assert calcul_taux_horaire(profile) == 100


def test_calcul_cout():

    profile = build_profile()

    assert (
        calcul_cout(
            10,
            profile,
        )
        == 1000
    )


def test_calcul_cout_total():

    assert (
        calcul_cout_total(
            100,
            200,
            300,
        )
        == 600
    )


def test_calcul_estimation_complete():

    profile = build_profile()

    project = ProjectParameters(
        nb_lignes=10,
        nb_supports=4,
        nb_vannes=2,
        nb_brides=10,
        nb_connexions_equipements=3,
    )

    deliverables = Deliverables(
        rapport_calcul=1,
        notes_supports=1,
        notes_equipements=1,
        plans_supports=1,
        presentation_client=1,
    )

    reviews = ReviewMetrics(
        nb_revues_internes=2,
        nb_revues_client=1,
        nb_aller_retour=1,
    )

    result = calcul_estimation(
        project,
        deliverables,
        reviews,
        profile,
    )

    assert result["effort_total_h"] > 0

    assert result["cout_total"] > 0

    assert result["taux_horaire"] == 100

    assert "effort_modelisation_h" in result

    assert "effort_redaction_h" in result

    assert "effort_verification_h" in result
