import pytest

from src.models.project import Project
from src.services.project_service import ProjectService
from src.utils.exceptions import ValidationError


def test_project_name_too_long():

    service = ProjectService()

    project = Project(
        nom="ABCDEFGHIJKLMNOPQRSTU",
        client="EDF",
    )

    with pytest.raises(ValidationError):
        service._validate_project(project)
