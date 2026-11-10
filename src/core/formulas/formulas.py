# Bibliothèque des formules métier

from src.models.deliverables import Deliverables
from src.models.project_parameters import ProjectParameters
from src.models.review_metrics import ReviewMetrics
from src.models.user_profile import UserProfile

# ==========================================================
# MODELISATION
# ==========================================================


def effort_lignes(
    nb_lignes: int,
    heure_par_ligne: float,
) -> float:
    return nb_lignes * heure_par_ligne


def effort_supports(
    nb_supports: int,
    heure_par_support: float,
) -> float:
    return nb_supports * heure_par_support


def effort_vannes(
    nb_vannes: int,
    heure_par_vanne: float,
) -> float:
    return nb_vannes * heure_par_vanne


def effort_brides(
    nb_brides: int,
    heure_par_bride: float,
) -> float:
    return nb_brides * heure_par_bride


def effort_equipements(
    nb_connexions: int,
    heure_par_equipement: float,
) -> float:
    return nb_connexions * heure_par_equipement


# ==========================================================
# LIVRABLES
# ==========================================================


def effort_rapport_calcul(
    nb_rapports: int,
    heure_par_note: float,
) -> float:
    return nb_rapports * heure_par_note


def effort_notes_supports(
    nb_notes: int,
    heure_par_note: float,
) -> float:
    return nb_notes * heure_par_note


def effort_notes_equipements(
    nb_notes: int,
    heure_par_note: float,
) -> float:
    return nb_notes * heure_par_note


def effort_plans_supports(
    nb_plans: int,
    heure_par_note: float,
) -> float:
    return nb_plans * heure_par_note


def effort_presentation_client(
    nb_presentations: int,
    heure_par_presentation: float,
) -> float:
    return nb_presentations * heure_par_presentation


# ==========================================================
# REVUES / VERIFICATIONS
# ==========================================================


def effort_revue_interne(
    nb_revues: int,
    heure_par_verification: float,
) -> float:
    return nb_revues * heure_par_verification


def effort_revue_client(
    nb_revues: int,
    heure_par_verification: float,
) -> float:
    return nb_revues * heure_par_verification


def effort_aller_retour(
    nb_allers_retours: int,
    heure_par_verification: float,
) -> float:
    return nb_allers_retours * heure_par_verification


# ==========================================================
# CHARGES GLOBALES
# ==========================================================


def calcul_effort_modelisation(
    project: ProjectParameters,
    profile: UserProfile,
) -> float:
    """
    Charge de modélisation.
    """

    return (
        effort_lignes(
            project.nb_lignes,
            profile.heure_par_ligne,
        )
        + effort_supports(
            project.nb_supports,
            profile.heure_par_support,
        )
        + effort_vannes(
            project.nb_vannes,
            profile.heure_par_vanne,
        )
        + effort_brides(
            project.nb_brides,
            profile.heure_par_bride,
        )
        + effort_equipements(
            project.nb_connexions_equipements,
            profile.heure_par_equipement,
        )
    )


def calcul_effort_redaction(
    deliverables: Deliverables,
    profile: UserProfile,
) -> float:
    """
    Charge documentaire.
    """

    return (
        effort_rapport_calcul(
            deliverables.rapport_calcul,
            profile.heure_par_note_de_calcul,
        )
        + effort_notes_supports(
            deliverables.notes_supports,
            profile.heure_par_note_de_calcul,
        )
        + effort_notes_equipements(
            deliverables.notes_equipements,
            profile.heure_par_note_de_calcul,
        )
        + effort_plans_supports(
            deliverables.plans_supports,
            profile.heure_par_note_de_calcul,
        )
        + effort_presentation_client(
            deliverables.presentation_client,
            profile.heure_par_presentation,
        )
    )


def calcul_effort_verification(
    reviews: ReviewMetrics,
    profile: UserProfile,
) -> float:
    """
    Charge liée aux revues.
    """

    return (
        effort_revue_interne(
            reviews.nb_revues_internes,
            profile.heure_par_verification,
        )
        + effort_revue_client(
            reviews.nb_revues_client,
            profile.heure_par_verification,
        )
        + effort_aller_retour(
            reviews.nb_aller_retour,
            profile.heure_par_verification,
        )
    )


# ==========================================================
# CONSOLIDATION
# ==========================================================


def calcul_effort_total(
    effort_modelisation: float,
    effort_redaction: float,
    effort_verification: float,
) -> float:
    return effort_modelisation + effort_redaction + effort_verification


# ==========================================================
# COUTS
# ==========================================================


def calcul_taux_horaire(
    profile: UserProfile,
) -> float:
    """
    Conversion TJM -> taux horaire.
    """

    return profile.taux_journalier / profile.heures_par_jour


def calcul_cout(
    effort_h: float,
    profile: UserProfile,
) -> float:
    """
    Coût d'une activité.
    """

    return effort_h * calcul_taux_horaire(profile)


def calcul_cout_total(
    cout_modelisation: float,
    cout_redaction: float,
    cout_verification: float,
) -> float:
    return cout_modelisation + cout_redaction + cout_verification


# ==========================================================
# CALCUL COMPLET
# ==========================================================


def calcul_estimation(
    project: ProjectParameters,
    deliverables: Deliverables,
    reviews: ReviewMetrics,
    profile: UserProfile,
) -> dict:
    """
    Fonction de haut niveau.
    Retourne tous les résultats principaux.
    """

    effort_modelisation = calcul_effort_modelisation(
        project,
        profile,
    )

    effort_redaction = calcul_effort_redaction(
        deliverables,
        profile,
    )

    effort_verification = calcul_effort_verification(
        reviews,
        profile,
    )

    effort_total = calcul_effort_total(
        effort_modelisation,
        effort_redaction,
        effort_verification,
    )

    cout_modelisation = calcul_cout(
        effort_modelisation,
        profile,
    )

    cout_redaction = calcul_cout(
        effort_redaction,
        profile,
    )

    cout_verification = calcul_cout(
        effort_verification,
        profile,
    )

    cout_total = calcul_cout_total(
        cout_modelisation,
        cout_redaction,
        cout_verification,
    )

    return {
        "effort_modelisation_h": effort_modelisation,
        "effort_redaction_h": effort_redaction,
        "effort_verification_h": effort_verification,
        "effort_total_h": effort_total,
        "cout_modelisation": cout_modelisation,
        "cout_redaction": cout_redaction,
        "cout_verification": cout_verification,
        "cout_total": cout_total,
        "taux_horaire": calcul_taux_horaire(profile),
    }
