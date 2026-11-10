# Dataclass représentant un profil utilisateur
# Taux journalier
# Productivité
# Paramètres personnalisésf
# user_profile.py

from dataclasses import dataclass


@dataclass(slots=True)
class UserProfile:
    """
    Profil utilisateur personnalisé.
    Permet de surcharger les temps standards.
    """

    id: int | None = None

    nom: str = ""
    description: str = ""

    taux_journalier: float = 650.0
    heures_par_jour: float = 7.0
    facteur_productivite: float = 1.0

    # Modélisation
    heure_par_ligne: float = 0.40
    heure_par_support: float = 0.20
    heure_par_vanne: float = 0.10
    heure_par_boite_a_ressort: float = 0.20
    heure_compensateur: float = 1.00
    heure_par_bride: float = 0.10
    heure_par_equipement: float = 0.10

    # Livrables
    heure_par_note_de_calcul: float = 4.0
    heure_par_presentation: float = 2.0

    # Vérification
    heure_par_verification: float = 1.0
