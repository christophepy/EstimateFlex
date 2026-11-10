# Point d'entrée de l'application
# Initialise l'environnement
# Charge la configuration
# Lance PyQt
# Crée MainWindow v1.0
"""
EstimateFlex v1.0
Point d'entrée principal
"""

from __future__ import annotations

import logging
import sys
import traceback

from PyQt6.QtWidgets import QApplication, QMessageBox

from src.config.paths import EnsureDirectories
from src.persistence.database import Database
from src.ui.main_window import MainWindow

APP_NAME = "EstimateFlex"
APP_VERSION = "1.0"


def configure_logging() -> None:
    """Configure le système de logs."""

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
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
        traceback.format_exception(exc_type, exc_value, exc_traceback)
    )

    logging.error(error_message)

    QMessageBox.critical(None, "Erreur critique", str(exc_value))


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

    window = MainWindow()
    window.show()

    logging.info("Interface chargée")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
