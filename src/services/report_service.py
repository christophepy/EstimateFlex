# Génération rapports
# src/services/report_service.py

from __future__ import annotations

from src.persistence.estimation_repository import (
    EstimationRepository,
)


class ReportService:
    """
    Service de gestion des rapports.
    """

    def __init__(self):

        self.repository = EstimationRepository()

    def get_available_estimations(
        self,
    ):

        estimations = self.repository.get_all()

        print(f"Reports : {len(estimations)} estimation(s)")

        return estimations

    def generate_pdf(
        self,
        estimation,
        filepath,
    ):

        raise NotImplementedError("Export PDF à implémenter.")

    def generate_excel(
        self,
        estimation,
        filepath,
    ):

        raise NotImplementedError("Export Excel à implémenter.")
