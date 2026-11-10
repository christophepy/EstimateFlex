import pytest

from src.models.user_profile import (
    UserProfile,
)
from src.services.profile_service import (
    ProfileService,
)


class FakeRepository:

    def __init__(self):

        self.by_name = {}
        self.by_id = {}

    def get_by_name(
        self,
        name,
    ):
        return self.by_name.get(name)

    def get_by_id(
        self,
        profile_id,
    ):
        return self.by_id.get(profile_id)

    def create(
        self,
        profile,
    ):
        return profile

    def update(
        self,
        profile,
    ):
        return True

    def delete(
        self,
        profile_id,
    ):
        return True

    def get_all(
        self,
    ):
        return list(self.by_id.values())


def build_profile():

    return UserProfile(
        nom="Senior",
        description="Profil test",
    )


def test_create_profile_success():

    repo = FakeRepository()

    service = ProfileService(repo)

    profile = build_profile()

    result = service.create_profile(profile)

    assert result == profile


def test_create_profile_name_required():

    repo = FakeRepository()

    service = ProfileService(repo)

    profile = UserProfile(
        nom="",
        description="Test",
    )

    with pytest.raises(ValueError):
        service.create_profile(profile)


def test_create_profile_duplicate():

    repo = FakeRepository()

    profile = build_profile()

    repo.by_name[profile.nom] = profile

    service = ProfileService(repo)

    with pytest.raises(ValueError):
        service.create_profile(profile)


def test_update_profile_without_id():

    repo = FakeRepository()

    service = ProfileService(repo)

    profile = build_profile()

    with pytest.raises(ValueError):
        service.update_profile(profile)


def test_update_profile_unknown():

    repo = FakeRepository()

    service = ProfileService(repo)

    profile = build_profile()
    profile.id = 10

    with pytest.raises(ValueError):
        service.update_profile(profile)


def test_delete_profile_unknown():

    repo = FakeRepository()

    service = ProfileService(repo)

    with pytest.raises(ValueError):
        service.delete_profile(99)


def test_get_profile():

    repo = FakeRepository()

    profile = build_profile()

    profile.id = 1

    repo.by_id[1] = profile

    service = ProfileService(repo)

    result = service.get_profile(1)

    assert result == profile


def test_get_profile_by_name():

    repo = FakeRepository()

    profile = build_profile()

    repo.by_name[profile.nom] = profile

    service = ProfileService(repo)

    result = service.get_profile_by_nom("Senior")

    assert result == profile


def test_validate_profile_ok():

    service = ProfileService()

    profile = build_profile()

    valid, errors = service.validate_profile(profile)

    assert valid is True

    assert not errors


def test_validate_profile_name_missing():

    service = ProfileService()

    profile = UserProfile(
        nom="",
        description="Test",
    )

    valid, errors = service.validate_profile(profile)

    assert valid is False

    assert len(errors) > 0


def test_count_profiles():

    repo = FakeRepository()

    p1 = build_profile()
    p1.id = 1

    p2 = UserProfile(
        nom="Expert",
        description="Test",
    )
    p2.id = 2

    repo.by_id[1] = p1
    repo.by_id[2] = p2

    service = ProfileService(repo)

    assert service.count_profiles() == 2
