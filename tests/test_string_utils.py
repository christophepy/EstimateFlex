from src.utils.string_utils import normalize_name


def test_ignore_case():
    assert normalize_name("HPC") == normalize_name("hpc")


def test_ignore_accents():
    assert normalize_name("Réaliste") == normalize_name("Realiste")


def test_ignore_underscore():
    assert normalize_name("HPC_D") == normalize_name("HPC D")


def test_ignore_dash():
    assert normalize_name("HPC-D") == normalize_name("HPC D")


def test_ignore_multiple_spaces():
    assert normalize_name("HPC   D") == normalize_name("HPC D")


def test_ignore_leading_trailing_spaces():
    assert normalize_name("  HPC D  ") == normalize_name("HPC D")
