from src.utils.string_utils import normalize_name


def test_scenario_normalization():

    assert normalize_name("Réaliste") == normalize_name("Realiste")


def test_scenario_separator_normalization():

    assert normalize_name("CLIENT_A") == normalize_name("CLIENT-A")
