from src.persistence.profile_repository import ProfileRepository


def test_default_profiles_exist():

    assert ProfileRepository.get_by_name("Junior") is not None

    assert ProfileRepository.get_by_name("Senior") is not None

    assert ProfileRepository.get_by_name("Expert") is not None
