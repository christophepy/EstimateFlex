# src/repositories/settings_repository.py
"""
Repository des paramètres.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.models.app_settings import AppSettings


class SettingsRepository:
    """
    Repository de gestion des paramètres globaux.
    Stockage dans data/settings.json.
    """

    def __init__(self, data_dir: str | Path = "data") -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.file_path = self.data_dir / "settings.json"

    def load(self) -> AppSettings:
        """
        Charge les paramètres.
        Crée automatiquement le fichier avec les valeurs
        par défaut s'il n'existe pas.
        """
        if not self.file_path.exists():
            settings = AppSettings()
            self.save(settings)
            return settings

        try:
            with open(self.file_path, encoding="utf-8") as f:
                data = json.load(f)

            return AppSettings.from_dict(data)

        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            settings = AppSettings()
            self.save(settings)
            return settings

    def save(self, settings: AppSettings) -> None:
        """
        Sauvegarde les paramètres.
        """
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(
                settings.to_dict(),
                f,
                ensure_ascii=False,
                indent=4,
            )

    def reset(self) -> AppSettings:
        """
        Réinitialise les paramètres aux valeurs par défaut.
        """
        settings = AppSettings()
        self.save(settings)
        return settings
