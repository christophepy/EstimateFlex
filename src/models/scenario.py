# src/models/scenario.py

from dataclasses import dataclass


@dataclass(slots=True)
class Scenario:
    id: int | None = None

    nom: str = ""
    description: str = ""

    facteur_productivite: float = 1.0
    facteur_risque: float = 1.0
    facteur_disponibilite: float = 1.0

    actif: bool = True
