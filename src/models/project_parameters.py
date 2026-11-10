# Données d'entrée du projet
# Nb API
# Nb écrans
# Nb rapports
# Nb règles métier

from dataclasses import dataclass


@dataclass(slots=True)
class ProjectParameters:
    """
    Données techniques du projet.
    """

    nb_lignes: int = 0
    nb_supports: int = 0
    nb_vannes: int = 0
    nb_brides: int = 0
    nb_compensateur: int = 0
    nb_connexions_equipements: int = 0
    nb_soudures: int = 0
