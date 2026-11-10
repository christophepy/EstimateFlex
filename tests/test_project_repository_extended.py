from src.persistence.project_repository import ProjectRepository


def test_repository_creation():

    repo = ProjectRepository()

    assert repo is not None


def test_list_projects_returns_list():

    repo = ProjectRepository()

    result = repo.list_projects()

    assert isinstance(
        result,
        list,
    )


def test_count_returns_int():

    repo = ProjectRepository()

    result = repo.count()

    assert isinstance(
        result,
        int,
    )


def test_exists_unknown():

    repo = ProjectRepository()

    assert repo.exists("DOES_NOT_EXIST") is False


def test_get_unknown_project():

    repo = ProjectRepository()

    assert repo.get_by_name("UNKNOWN") is None
