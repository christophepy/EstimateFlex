from src.persistence.project_repository import ProjectRepository


def test_exists_is_case_insensitive():

    repo = ProjectRepository()

    assert repo._name_exists("hpc") == repo._name_exists("HPC")
