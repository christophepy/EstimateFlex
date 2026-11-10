from src.models.scenario import (
    Scenario,
)
from src.persistence.scenario_repository import (
    ScenarioRepository,
)


def test_count_returns_int():

    result = ScenarioRepository.count()

    assert isinstance(
        result,
        int,
    )


def test_get_all_returns_list():

    result = ScenarioRepository.get_all()

    assert isinstance(
        result,
        list,
    )


def test_get_unknown_scenario():

    result = ScenarioRepository.get_by_id(-999999)

    assert result is None


def test_get_unknown_name():

    result = ScenarioRepository.get_by_name("UNKNOWN")

    assert result is None


def test_update_unknown():

    scenario = Scenario(
        id=-999,
        nom="TEST",
        description="",
        facteur_productivite=1.0,
        facteur_risque=1.0,
        facteur_disponibilite=1.0,
        actif=True,
    )

    result = ScenarioRepository.update(scenario)

    assert result is False
