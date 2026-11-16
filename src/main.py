"""
EstimateFlex v2.1a
Point d'entrée principal
"""

from __future__ import annotations

import logging
import sys
import traceback

from PyQt6.QtWidgets import QApplication, QMessageBox

from src.config.paths import EnsureDirectories
from src.persistence.database import Database
from src.persistence.settings_repository import SettingsRepository
from src.services.currency_service import CurrencyService
from src.services.settings_service import SettingsService
from src.ui.main_window import MainWindow

APP_NAME = "EstimateFlex"
APP_VERSION = "2.1a"


def configure_logging() -> None:
    """Configure le système de logs."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def initialize_application() -> None:
    """
    Initialisation globale.
    """

    logging.info("Initialisation EstimateFlex")

    EnsureDirectories()

    db = Database()
    db.initialize()

    logging.info("Base de données initialisée")


def handle_exception(exc_type, exc_value, exc_traceback):
    """
    Gestionnaire global d'erreurs.
    """

    error_message = "".join(
        traceback.format_exception(
            exc_type,
            exc_value,
            exc_traceback,
        )
    )

    logging.error(error_message)

    QMessageBox.critical(
        None,
        "Erreur critique",
        str(exc_value),
    )


def main() -> int:
    """
    Point d'entrée principal.
    """

    configure_logging()

    sys.excepthook = handle_exception

    logging.info(
        "Démarrage %s v%s",
        APP_NAME,
        APP_VERSION,
    )

    initialize_application()

    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)

    # Paramètres application
    settings_repository = SettingsRepository()
    settings_service = SettingsService(settings_repository)

    # Service devises
    currency_service = CurrencyService(settings_service)

    # Fenêtre principale
    window = MainWindow(
        settings_service=settings_service,
        currency_service=currency_service,
    )

    window.show()

    logging.info("Interface chargée")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
