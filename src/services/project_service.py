from __future__ import annotations

from src.models.project import Project
from src.persistence.project_repository import (
    ProjectRepository,
)
from src.utils.exceptions import ValidationError
from src.utils.string_utils import normalize_name


class ProjectService:
    """
    Service métier des projets.
    """

    def __init__(
        self,
        repository: ProjectRepository | None = None,
    ):
        self.repository = repository or ProjectRepository()

    # ============================================================
    # CRUD
    # ============================================================

    def create_project(
        self,
        project: Project,
    ) -> Project:

        self._validate_project(project)

        if self.repository.exists(project.nom):
            raise ValidationError(f"Le projet '{project.nom}' existe déjà.")

        return self.repository.save(project)

    def update_project(
        self,
        project: Project,
    ) -> Project:

        self._validate_project(project)

        return self.repository.update(project)

    def delete_project(
        self,
        project_nom: str,
    ) -> bool:

        project = self.repository.get_by_name(project_nom)

        if project is None:
            raise ValidationError(f"Projet introuvable : {project_nom}")

        return self.repository.delete(project_nom)

    def get_project(
        self,
        project_nom: str,
    ) -> Project | None:

        return self.repository.get_by_name(project_nom)

    def get_project_by_nom(
        self,
        nom: str,
    ) -> Project | None:

        return self.repository.get_by_name(nom)

    def get_all_projects(
        self,
    ) -> list[Project]:

        return self.repository.get_all()

    # ============================================================
    # Recherche
    # ============================================================

    def search_projects(
        self,
        keyword: str,
    ) -> list[Project]:

        keyword = keyword.lower().strip()

        results = []

        for project in self.repository.get_all():

            description = getattr(
                project,
                "description",
                "",
            )

            if keyword in project.nom.lower() or keyword in description.lower():
                results.append(project)

        return results

    # ============================================================
    # Indicateurs
    # ============================================================

    def count_projects(self) -> int:

        return len(self.repository.get_all())

    def total_estimated_cost(
        self,
    ) -> float:

        total = 0.0

        for project in self.repository.get_all():

            total += getattr(
                project,
                "estimated_cost",
                0.0,
            )

        return round(
            total,
            2,
        )

    def total_estimated_days(
        self,
    ) -> float:

        total = 0.0

        for project in self.repository.get_all():

            total += getattr(
                project,
                "estimated_days",
                0.0,
            )

        return round(
            total,
            2,
        )

    def total_estimated_hours(
        self,
    ) -> float:

        total = 0.0

        for project in self.repository.get_all():

            total += getattr(
                project,
                "estimated_hours",
                0.0,
            )

        return round(
            total,
            2,
        )

    # ============================================================
    # Préparation estimation
    # ============================================================

    def build_estimation_context(
        self,
        project_nom: str,
    ) -> dict:

        project = self.get_project(project_nom)

        if project is None:

            raise ValidationError(f"Projet introuvable : " f"{project_nom}")

        return {
            "project_nom": project.nom,
            "deliverables": project.deliverables,
            "parameters": project.parameters,
            "reviews": project.reviews,
        }

    # ============================================================
    # Validation
    # ============================================================

    def _validate_project(
        self,
        project: Project,
    ) -> None:

        nom = project.nom.strip()

        description = (project.description or "").strip()

        if len(description) > 200:
            raise ValidationError("La description est limitée à 200 caractères.")

        normalized = normalize_name(nom)

        if normalized in {
            "",
            "-",
            "_",
        }:
            raise ValidationError("Nom de projet invalide.")

        if not nom:

            raise ValidationError("Le nom du projet est obligatoire.")

        if len(nom) < 3:

            raise ValidationError(
                "Le nom du projet doit comporter au moins "
                "3 caractères (ex : ASG, RIS, EPR)."
            )

        if len(nom) > 20:
            raise ValidationError("Le nom du projet est limité à 20 caractères.")

        if hasattr(project, "complexity"):

            allowed = {
                "LOW",
                "MEDIUM",
                "HIGH",
                "VERY_HIGH",
            }

            value = str(project.complexity).upper()

            if value not in allowed:

                raise ValidationError(f"Complexité invalide : " f"{project.complexity}")

    # ============================================================
    # Dashboard
    # ============================================================

    def dashboard_summary(
        self,
    ) -> dict:

        projects = self.get_all_projects()

        return {
            "projects_count": len(projects),
            "total_hours": self.total_estimated_hours(),
            "total_days": self.total_estimated_days(),
            "total_cost": self.total_estimated_cost(),
        }
