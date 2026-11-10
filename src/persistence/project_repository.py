# src/persistence/project_repository.py

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from src.models.deliverables import Deliverables
from src.models.project import Project
from src.models.project_parameters import ProjectParameters
from src.models.review_metrics import ReviewMetrics
from src.utils.string_utils import normalize_name


class ProjectRepository:
    """
    Repository JSON des projets.
    """

    def __init__(
        self,
        storage_dir: str | Path = "data/projects",
    ) -> None:

        self.storage_dir = Path(storage_dir)

        self.storage_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _name_exists(
        self,
        project_nom: str,
    ) -> bool:
        """
        Vérifie si un projet existe déjà
        en ignorant casse et accents.
        """

        normalized = normalize_name(project_nom)

        for project in self.get_all():

            if normalize_name(project.nom) == normalized:
                return True

        return False

    # ============================================================
    # CRUD
    # ============================================================

    def save(
        self,
        project: Project,
    ) -> Project:
        """
        Sauvegarde un projet.
        """

        data = {
            "nom": project.nom,
            "client": project.client,
            "description": project.description,
            "parameters": asdict(project.parameters),
            "deliverables": asdict(project.deliverables),
            "reviews": asdict(project.reviews),
        }

        file_path = self.storage_dir / f"{project.nom}.json"

        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )

        return project

    def delete(
        self,
        project_nom: str,
    ) -> bool:
        """
        Suppression d'un projet.
        """

        file_path = self.storage_dir / f"{project_nom}.json"

        if not file_path.exists():
            return False

        file_path.unlink()

        return True

    # ============================================================
    # Recherche
    # ============================================================

    def load(
        self,
        project_nom: str,
    ) -> Project:

        file_path = self.storage_dir / f"{project_nom}.json"

        if not file_path.exists():
            raise FileNotFoundError(f"Projet introuvable : {file_path}")

        with open(
            file_path,
            encoding="utf-8",
        ) as f:

            data = json.load(f)

        return Project(
            nom=data["nom"],
            client=data.get("client", ""),
            description=data.get(
                "description",
                "",
            ),
            parameters=ProjectParameters(
                **data.get(
                    "parameters",
                    {},
                )
            ),
            deliverables=Deliverables(
                **data.get(
                    "deliverables",
                    {},
                )
            ),
            reviews=ReviewMetrics(
                **data.get(
                    "reviews",
                    {},
                )
            ),
        )

    def get_by_name(
        self,
        nom: str,
    ) -> Project | None:

        try:
            return self.load(nom)
        except FileNotFoundError:
            return None

    def get_by_id(
        self,
        project_id: int,
    ) -> Project | None:
        """
        Compatibilité temporaire.
        """

        for project in self.get_all():

            if project.id == project_id:
                return project
        return None

    def get_all(
        self,
    ) -> list[Project]:
        """
        Retourne tous les projets.
        """

        projects = []

        for file in sorted(self.storage_dir.glob("*.json")):

            try:
                project = self.load(file.stem)

                project.id = len(projects) + 1

                projects.append(project)

            except Exception as exc:  # pylint: disable=broad-exception-caught
                print(f"ERREUR : {file.name}")
                print(f"Type : {type(exc).__name__}")
                print(f"Message : {exc}")

        return projects

    def exists(
        self,
        project_nom: str,
    ) -> bool:
        """
        Vérifie l'existence d'un projet
        en ignorant casse et accents.
        """

        return self._name_exists(project_nom)

    def list_projects(
        self,
    ) -> list[str]:

        return sorted(file.stem for file in self.storage_dir.glob("*.json"))

    def update(
        self,
        project: Project,
    ) -> Project:
        """
        Mise à jour d'un projet.
        """

        return self.save(project)

    def count(self) -> int:
        """
        Nombre total de projets.
        """

        return len(self.get_all())
