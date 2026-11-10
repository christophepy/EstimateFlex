import pytest

from src.models.project import Project
from src.services.project_service import ProjectService
from src.utils.exceptions import ValidationError


def test_project_name_required():

    service = ProjectService()

    project = Project(
        nom="",
        client="EDF",
    )

    with pytest.raises(ValidationError):
        service.create_project(project)


def test_project_name_too_short():

    service = ProjectService()

    project = Project(
        nom="AB",
        client="EDF",
    )

    with pytest.raises(ValidationError):
        service.create_project(project)
