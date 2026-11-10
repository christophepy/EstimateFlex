"""
Exceptions métier EstimateFlex
"""


class EstimateFlexError(Exception):
    """Exception de base."""


class ValidationError(EstimateFlexError):
    """Erreur de validation."""


class DatabaseError(EstimateFlexError):
    """Erreur base de données."""


class EstimationError(EstimateFlexError):
    """Erreur moteur d'estimation."""


class ReportGenerationError(EstimateFlexError):
    """Erreur de génération de rapport."""
