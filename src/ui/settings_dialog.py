# src/ui/settings_dialog.py

from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.models.app_settings import AppSettings
from src.services.settings_service import SettingsService


class SettingsDialog(QDialog):
    """
    Fenêtre des paramètres de l'application.
    """

    def __init__(
        self,
        settings_service: SettingsService,
        parent=None,
    ):
        super().__init__(parent)

        self.settings_service = settings_service
        self.settings = self.settings_service.get()

        self.setWindowTitle("Paramètres")
        self.resize(600, 400)

        self._create_ui()
        self._load_settings()

    # ==========================================================
    # UI
    # ==========================================================

    def _create_ui(self):

        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()

        # --------------------------------------------------
        # Général
        # --------------------------------------------------

        general_tab = QWidget()
        general_layout = QFormLayout(general_tab)

        self.currency_combo = QComboBox()
        self.currency_combo.addItems(
            [
                "EUR",
                "CHF",
                "USD",
                "GBP",
            ]
        )

        self.export_directory_edit = QLineEdit()

        self.export_directory_btn = QPushButton("Parcourir...")

        self.export_directory_btn.clicked.connect(self._choose_export_directory)

        general_layout.addRow(
            "Devise",
            self.currency_combo,
        )

        export_widget = QWidget()

        export_layout = QHBoxLayout(export_widget)
        export_layout.setContentsMargins(0, 0, 0, 0)

        export_layout.addWidget(self.export_directory_edit)

        export_layout.addWidget(self.export_directory_btn)

        general_layout.addRow(
            "Répertoire exports",
            export_widget,
        )

        # --------------------------------------------------
        # Affichage
        # --------------------------------------------------

        display_tab = QWidget()
        display_layout = QFormLayout(display_tab)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(
            [
                "light",
                "dark",
                "system",
            ]
        )

        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)

        self.dashboard_kpis_check = QCheckBox("Afficher les KPI Dashboard")

        self.dashboard_charts_check = QCheckBox("Afficher les graphiques Dashboard")

        display_layout.addRow(
            "Thème",
            self.theme_combo,
        )

        display_layout.addRow(
            "Taille de police",
            self.font_size_spin,
        )

        display_layout.addRow(
            "",
            self.dashboard_kpis_check,
        )

        display_layout.addRow(
            "",
            self.dashboard_charts_check,
        )

        # --------------------------------------------------
        # Tabs
        # --------------------------------------------------

        self.tabs.addTab(
            general_tab,
            "Général",
        )

        self.tabs.addTab(
            display_tab,
            "Affichage",
        )

        layout.addWidget(self.tabs)

        # --------------------------------------------------
        # Boutons
        # --------------------------------------------------

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(self._save)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)

    # ==========================================================
    # Chargement
    # ==========================================================

    def _load_settings(self):

        self.currency_combo.setCurrentText(self.settings.currency)

        self.export_directory_edit.setText(self.settings.export_directory)

        self.theme_combo.setCurrentText(self.settings.theme)

        self.font_size_spin.setValue(self.settings.font_size)

        self.dashboard_kpis_check.setChecked(self.settings.show_dashboard_kpis)

        self.dashboard_charts_check.setChecked(self.settings.show_dashboard_charts)

    def _choose_export_directory(self):

        directory = QFileDialog.getExistingDirectory(
            self,
            "Choisir le répertoire d'exports",
            self.export_directory_edit.text(),
        )

        if directory:
            self.export_directory_edit.setText(directory)

    # ==========================================================
    # Sauvegarde
    # ==========================================================

    def _save(self):

        try:

            settings = AppSettings(
                currency=self.currency_combo.currentText(),
                export_directory=self.export_directory_edit.text().strip(),
                theme=self.theme_combo.currentText(),
                font_size=self.font_size_spin.value(),
                show_dashboard_kpis=self.dashboard_kpis_check.isChecked(),
                show_dashboard_charts=self.dashboard_charts_check.isChecked(),
            )

            self.settings_service.save(settings)

            parent = self.parent()

            if parent is not None and hasattr(parent, "reload_settings"):
                parent.reload_settings()

            QMessageBox.information(
                self,
                "Paramètres",
                "Paramètres sauvegardés.",
            )

            self.accept()

        except ValueError as exc:

            QMessageBox.critical(
                self,
                "Erreur",
                str(exc),
            )
