# src/services/settings_service.py

from __future__ import annotations

from src.models.app_settings import AppSettings
from src.persistence.settings_repository import SettingsRepository


class SettingsService:
    """
    Service de gestion des paramètres globaux.
    """

    def __init__(self, repository: SettingsRepository) -> None:
        self.persistence = repository

    def get(self) -> AppSettings:
        """
        Retourne les paramètres courants.
        """
        return self.persistence.load()

    def save(self, settings: AppSettings) -> None:
        """
        Valide puis sauvegarde les paramètres.
        """
        self._validate(settings)
        self.persistence.save(settings)

    def reset(self) -> AppSettings:
        """
        Réinitialise les paramètres.
        """
        return self.persistence.reset()

    def update(self, **kwargs) -> AppSettings:
        """
        Mise à jour partielle des paramètres.
        """
        settings = self.get()

        for key, value in kwargs.items():
            if hasattr(settings, key):
                setattr(settings, key, value)

        self.save(settings)

        return settings

    def _validate(self, settings: AppSettings) -> None:
        """
        Validation métier.
        """

        if settings.font_size < 8:
            raise ValueError("La taille de police doit être supérieure ou égale à 8.")

        if settings.theme not in (
            "light",
            "dark",
            "system",
        ):
            raise ValueError("Le thème doit être 'light', 'dark' ou 'system'.")

        if not settings.currency.strip():
            raise ValueError("La devise est obligatoire.")

        supported_currencies = {
            "EUR",
            "USD",
            "CHF",
            "GBP",
        }

        if settings.currency not in supported_currencies:
            raise ValueError(f"Devise non supportée : {settings.currency}")

        if settings.export_directory and not isinstance(
            settings.export_directory,
            str,
        ):
            raise ValueError("Le répertoire d'export est invalide.")
