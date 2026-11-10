# src/ui/scenarios_tab.py

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.services.scenario_service import ScenarioService
from src.ui.scenario_dialog import ScenarioDialog


class ScenariosTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.service = ScenarioService()

        self._build_ui()
        self.load_scenarios()

    def _build_ui(self):

        layout = QVBoxLayout(self)

        # =====================================================
        # BOUTONS
        # =====================================================

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Ajouter")
        self.edit_button = QPushButton("Modifier")
        self.delete_button = QPushButton("Supprimer")
        self.refresh_button = QPushButton("Rafraîchir")

        self.add_button.clicked.connect(self.add_scenario)

        self.edit_button.clicked.connect(self.edit_scenario)

        self.delete_button.clicked.connect(self.delete_scenario)

        self.refresh_button.clicked.connect(self.load_scenarios)

        button_layout.addWidget(self.add_button)

        button_layout.addWidget(self.edit_button)

        button_layout.addWidget(self.delete_button)

        button_layout.addStretch()

        button_layout.addWidget(self.refresh_button)

        # =====================================================
        # TABLEAU
        # =====================================================

        self.table = QTableWidget()

        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.table.setStyleSheet("""
            QTableWidget::item {
                border: none;
            }

            QTableWidget::item:selected {
                background-color: #DCEEFF;
                color: black;
            }

            QTableWidget::item:focus {
                outline: 0;
                border: none;
            }
            """)

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels(
            [
                "Nom",
                "Productivité",
                "Risque",
                "Disponibilité",
                "Actif",
            ]
        )

        self.table.itemSelectionChanged.connect(self._show_details)

        # =====================================================
        # DETAILS
        # =====================================================

        details_group = QGroupBox("Détails du scénario")

        details_layout = QVBoxLayout()

        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)

        details_layout.addWidget(self.details_text)

        details_group.setLayout(details_layout)

        # =====================================================
        # ASSEMBLAGE
        # =====================================================

        layout.addLayout(button_layout)
        layout.addWidget(self.table)
        layout.addWidget(details_group)

    def load_scenarios(self):

        try:

            self.scenarios = self.service.get_all_scenarios()

            self.table.setRowCount(len(self.scenarios))

            for row, scenario in enumerate(self.scenarios):

                self.table.setItem(
                    row,
                    0,
                    QTableWidgetItem(scenario.nom),
                )

                self.table.setItem(
                    row,
                    1,
                    QTableWidgetItem(f"{scenario.facteur_productivite:.2f}"),
                )

                self.table.setItem(
                    row,
                    2,
                    QTableWidgetItem(f"{scenario.facteur_risque:.2f}"),
                )

                self.table.setItem(
                    row,
                    3,
                    QTableWidgetItem(f"{scenario.facteur_disponibilite:.2f}"),
                )

                self.table.setItem(
                    row,
                    4,
                    QTableWidgetItem("Oui" if scenario.actif else "Non"),
                )

            self.table.resizeColumnsToContents()

            if self.scenarios:
                self.table.selectRow(0)

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Erreur",
                str(exc),
            )

    def get_selected_scenario(self):

        row = self.table.currentRow()

        if row < 0:
            return None

        return self.scenarios[row]

    def add_scenario(self):

        dialog = ScenarioDialog(self)

        if dialog.exec():

            try:

                scenario = dialog.get_scenario()

                self.service.create_scenario(scenario)

                self.load_scenarios()

            except Exception as exc:

                QMessageBox.critical(
                    self,
                    "Erreur",
                    str(exc),
                )

    def edit_scenario(self):

        scenario = self.get_selected_scenario()

        if scenario is None:

            QMessageBox.warning(self, "Scénario", "Sélectionnez un scénario.")

            return

        dialog = ScenarioDialog(
            self,
            scenario,
        )

        if dialog.exec():

            try:

                self.service.update_scenario(dialog.get_scenario())

                self.load_scenarios()

            except Exception as exc:

                QMessageBox.critical(
                    self,
                    "Erreur",
                    str(exc),
                )

    def delete_scenario(self):

        scenario = self.get_selected_scenario()

        if scenario is None:

            QMessageBox.warning(self, "Scénario", "Sélectionnez un scénario.")

            return

        reply = QMessageBox.question(
            self,
            "Suppression",
            (f"Supprimer le scénario " f"'{scenario.nom}' ?"),
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:

            self.service.delete_scenario(scenario.id)

            self.load_scenarios()

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Erreur",
                str(exc),
            )

    def _show_details(self):

        scenario = self.get_selected_scenario()

        if scenario is None:

            self.details_text.clear()

            return

        details = []

        details.append(f"Nom : {scenario.nom}")

        details.append("")

        details.append(f"Description : {scenario.description}")

        details.append("")

        details.append(
            f"Facteur productivité : " f"{scenario.facteur_productivite:.2f}"
        )

        details.append(f"Facteur risque : " f"{scenario.facteur_risque:.2f}")

        details.append(
            f"Facteur disponibilité : " f"{scenario.facteur_disponibilite:.2f}"
        )

        details.append("")

        details.append("Actif : " + ("Oui" if scenario.actif else "Non"))

        self.details_text.setPlainText("\n".join(details))

    def refresh(self):

        self.load_scenarios()
