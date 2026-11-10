from dataclasses import dataclass


@dataclass(slots=True)
class ReviewMetrics:

    nb_revues_internes: int = 0
    nb_revues_client: int = 0
    nb_aller_retour: int = 0
