# src/services/scenario_service.py


from src.models.scenario import Scenario
from src.persistence.scenario_repository import (
    ScenarioRepository,
)


class ScenarioService:

    def __init__(self):

        self.repository = ScenarioRepository()

    def get_all_scenarios(self) -> list[Scenario]:

        return self.repository.get_all()

    def get_scenario(
        self,
        scenario_id: int,
    ) -> Scenario | None:

        return self.repository.get_by_id(scenario_id)

    def get_by_name(
        self,
        nom: str,
    ) -> Scenario | None:

        return self.repository.get_by_name(nom)

    def create_scenario(
        self,
        scenario: Scenario,
    ) -> int:

        self._validate_scenario(scenario)

        existing = self.repository.get_by_name(scenario.nom)

        if existing:
            raise ValueError(f"Le scénario '{scenario.nom}' existe déjà.")

        return self.repository.create(scenario)

    def update_scenario(
        self,
        scenario: Scenario,
    ) -> None:

        self._validate_scenario(scenario)

        existing = self.repository.get_by_name(scenario.nom)

        if existing and existing.id != scenario.id:
            raise ValueError(f"Le scénario '{scenario.nom}' existe déjà.")

        if not self.repository.update(scenario):
            raise ValueError("Mise à jour impossible.")

    def delete_scenario(
        self,
        scenario_id: int,
    ) -> None:

        if not self.repository.delete(scenario_id):
            raise ValueError("Suppression impossible.")

    def count(self) -> int:

        return self.repository.count()

    def _validate_scenario(
        self,
        scenario: Scenario,
    ) -> None:

        if not scenario.nom.strip():
            raise ValueError("Le nom du scénario est obligatoire.")

        if len(scenario.nom.strip()) < 3:
            raise ValueError("Le nom du scénario est trop court.")

        if scenario.facteur_productivite <= 0:
            raise ValueError("Le facteur de productivité doit être supérieur à 0.")

        if scenario.facteur_risque <= 0:
            raise ValueError("Le facteur de risque doit être supérieur à 0.")

        if scenario.facteur_disponibilite <= 0:
            raise ValueError("Le facteur de disponibilité doit être supérieur à 0.")
