from src.persistence.scenario_repository import ScenarioRepository


def test_default_scenarios_exist():

    assert ScenarioRepository.get_by_name("Optimiste") is not None

    assert ScenarioRepository.get_by_name("Réaliste") is not None

    assert ScenarioRepository.get_by_name("Pessimiste") is not None
