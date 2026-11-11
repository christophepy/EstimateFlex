from dataclasses import dataclass, field

from .deliverables import Deliverables
from .project_parameters import ProjectParameters
from .review_metrics import ReviewMetrics


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

    deliverables: Deliverables = field(default_factory=Deliverables)

    reviews: ReviewMetrics = field(default_factory=ReviewMetrics)
