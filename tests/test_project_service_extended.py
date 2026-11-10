import pytest

from src.models.deliverables import (
    Deliverables,
)
from src.models.project import Project
from src.models.project_parameters import (
    ProjectParameters,
)
from src.models.review_metrics import (
    ReviewMetrics,
)
from src.services.project_service import (
    ProjectService,
)
from src.utils.exceptions import (
    ValidationError,
)


class FakeRepository:

    def __init__(self):

        self.projects = {}

    def get_by_name(
        self,
        name,
    ):
        return self.projects.get(name)

    def get_all(self):
        return list(self.projects.values())

    def save(
        self,
        project,
    ):
        self.projects[project.nom] = project

        return project

    def update(
        self,
        project,
    ):
        return project

    def delete(
        self,
        nom,
    ):
        return True


def build_project():

    return Project(
        nom="HPC",
        client="EDF",
        description="Test",
        parameters=ProjectParameters(),
        deliverables=Deliverables(),
        reviews=ReviewMetrics(),
    )


def test_get_project():

    repo = FakeRepository()

    project = build_project()

    repo.projects["HPC"] = project

    service = ProjectService(repo)

    assert service.get_project("HPC") == project


def test_delete_unknown_project():

    repo = FakeRepository()

    service = ProjectService(repo)

    with pytest.raises(ValidationError):
        service.delete_project("UNKNOWN")


def test_count_projects():

    repo = FakeRepository()

    repo.projects["A"] = build_project()
    repo.projects["B"] = build_project()

    service = ProjectService(repo)

    assert service.count_projects() == 2


def test_search_project_name():

    repo = FakeRepository()

    project = build_project()

    repo.projects["HPC"] = project

    service = ProjectService(repo)

    results = service.search_projects("hpc")

    assert len(results) == 1


def test_dashboard_summary():

    repo = FakeRepository()

    repo.projects["A"] = build_project()

    service = ProjectService(repo)

    summary = service.dashboard_summary()

    assert "projects_count" in summary
