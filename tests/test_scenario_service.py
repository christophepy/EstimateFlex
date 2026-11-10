import pytest

from src.models.scenario import (
    Scenario,
)
from src.services.scenario_service import (
    ScenarioService,
)


class FakeRepository:

    def __init__(self):

        self.by_id = {}
        self.by_name = {}

    def get_all(self):
        return list(self.by_id.values())

    def get_by_id(
        self,
        scenario_id,
    ):
        return self.by_id.get(scenario_id)

    def get_by_name(
        self,
        name,
    ):
        return self.by_name.get(name)

    def create(
        self,
        scenario,
    ):
        return 1

    def update(
        self,
        scenario,
    ):
        return True

    def delete(
        self,
        scenario_id,
    ):
        return True

    def count(self):
        return len(self.by_id)


def build_scenario():

    return Scenario(
        nom="Réaliste_Test",
        description="Test",
        facteur_productivite=1.0,
        facteur_risque=1.0,
        facteur_disponibilite=1.0,
        actif=True,
    )


def build_service():

    service = ScenarioService()

    service.repository = FakeRepository()

    return service


def test_get_all_scenarios():

    service = build_service()

    assert service.get_all_scenarios() == []


def test_get_scenario():

    service = build_service()

    scenario = build_scenario()
    scenario.id = 1

    service.repository.by_id[1] = scenario

    result = service.get_scenario(1)

    assert result == scenario


def test_get_by_name():

    service = build_service()

    scenario = build_scenario()

    service.repository.by_name[scenario.nom] = scenario

    result = service.get_by_name(scenario.nom)

    assert result == scenario


def test_create_scenario_success():

    service = build_service()

    scenario = build_scenario()

    scenario_id = service.create_scenario(scenario)

    assert scenario_id == 1


def test_create_scenario_duplicate():

    service = build_service()

    scenario = build_scenario()

    service.repository.by_name[scenario.nom] = scenario

    with pytest.raises(ValueError):
        service.create_scenario(scenario)


def test_update_scenario_duplicate():

    service = build_service()

    current = build_scenario()
    current.id = 1

    other = Scenario(
        id=2,
        nom=current.nom,
        description="",
        facteur_productivite=1.0,
        facteur_risque=1.0,
        facteur_disponibilite=1.0,
        actif=True,
    )

    service.repository.by_name[current.nom] = other

    with pytest.raises(ValueError):
        service.update_scenario(current)


def test_delete_failure():

    class RepoKO(FakeRepository):

        def delete(
            self,
            scenario_id,
        ):
            return False

    service = ScenarioService()

    service.repository = RepoKO()

    with pytest.raises(ValueError):
        service.delete_scenario(1)


def test_count():

    service = build_service()

    s1 = build_scenario()
    s1.id = 1

    s2 = build_scenario()
    s2.id = 2

    service.repository.by_id[1] = s1
    service.repository.by_id[2] = s2

    assert service.count() == 2


def test_validate_name_required():

    service = build_service()

    scenario = build_scenario()
    scenario.nom = ""

    with pytest.raises(ValueError):
        service._validate_scenario(scenario)


def test_validate_name_too_short():

    service = build_service()

    scenario = build_scenario()
    scenario.nom = "AB"

    with pytest.raises(ValueError):
        service._validate_scenario(scenario)


def test_validate_productivity():

    service = build_service()

    scenario = build_scenario()

    scenario.facteur_productivite = 0

    with pytest.raises(ValueError):
        service._validate_scenario(scenario)


def test_validate_risk():

    service = build_service()

    scenario = build_scenario()

    scenario.facteur_risque = 0

    with pytest.raises(ValueError):
        service._validate_scenario(scenario)


def test_validate_availability():

    service = build_service()

    scenario = build_scenario()

    scenario.facteur_disponibilite = 0

    with pytest.raises(ValueError):
        service._validate_scenario(scenario)
