from dataclasses import dataclass


@dataclass(slots=True)
class Deliverables:

    rapport_calcul: int = 0
    rapport_calcul_intermediare: int = 0
    fichier_resultat: int = 0

    notes_supports: int = 0
    notes_equipements: int = 0
    plans_supports: int = 0
    presentation_client: int = 0
    fichier_modele: int = 0
