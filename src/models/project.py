from dataclasses import dataclass, field

from .project_parameters import ProjectParameters


@dataclass(slots=True)
class Project:

    id: int | None = None

    nom: str = ""
    client: str = ""
    description: str = ""

    profile_nom: str = ""

    budget: float = 0.0

    status: str = "Draft"

    parameters: ProjectParameters = field(default_factory=ProjectParameters)

    deliverables: list[str] = field(default_factory=list)

    reviews: dict = field(default_factory=dict)
