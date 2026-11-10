# src/ui/scenario_dialog.py

from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
)

from src.models.scenario import Scenario


class ScenarioDialog(QDialog):

    def __init__(
        self,
        parent=None,
        scenario=None,
    ):
        super().__init__(parent)

        self.scenario = scenario

        self.setWindowTitle("Scénario")
        self.resize(500, 400)

        self._build_ui()
        self._load_scenario()

    def _build_ui(self):

        layout = QVBoxLayout(self)

        # =====================================================
        # INFORMATIONS
        # =====================================================

        info_group = QGroupBox("Informations")

        info_form = QFormLayout()

        self.nom_edit = QLineEdit()

        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)

        info_form.addRow(
            "Nom :",
            self.nom_edit,
        )

        info_form.addRow(
            "Description :",
            self.description_edit,
        )

        info_group.setLayout(info_form)

        # =====================================================
        # FACTEURS
        # =====================================================

        factors_group = QGroupBox("Facteurs d'estimation")

        factors_form = QFormLayout()

        self.productivite_edit = QDoubleSpinBox()
        self.productivite_edit.setRange(0.50, 2.00)
        self.productivite_edit.setDecimals(2)
        self.productivite_edit.setSingleStep(0.10)
        self.productivite_edit.setValue(1.00)

        self.risque_edit = QDoubleSpinBox()
        self.risque_edit.setRange(0.50, 3.00)
        self.risque_edit.setDecimals(2)
        self.risque_edit.setSingleStep(0.10)
        self.risque_edit.setValue(1.00)

        self.disponibilite_edit = QDoubleSpinBox()
        self.disponibilite_edit.setRange(0.10, 1.00)
        self.disponibilite_edit.setDecimals(2)
        self.disponibilite_edit.setSingleStep(0.10)
        self.disponibilite_edit.setValue(1.00)

        factors_form.addRow(
            "Facteur productivité :",
            self.productivite_edit,
        )

        factors_form.addRow(
            "Facteur risque :",
            self.risque_edit,
        )

        factors_form.addRow(
            "Facteur disponibilité :",
            self.disponibilite_edit,
        )

        factors_group.setLayout(factors_form)

        # =====================================================
        # ETAT
        # =====================================================

        state_group = QGroupBox("État")

        state_form = QFormLayout()

        self.actif_check = QCheckBox()
        self.actif_check.setChecked(True)

        state_form.addRow(
            "Scénario actif :",
            self.actif_check,
        )

        state_group.setLayout(state_form)

        # =====================================================
        # BOUTONS
        # =====================================================

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)

        buttons.rejected.connect(self.reject)

        # =====================================================
        # LAYOUT
        # =====================================================

        layout.addWidget(info_group)
        layout.addWidget(factors_group)
        layout.addWidget(state_group)
        layout.addWidget(buttons)

    def _load_scenario(self):

        if not self.scenario:
            return

        self.nom_edit.setText(self.scenario.nom)

        self.description_edit.setPlainText(self.scenario.description)

        self.productivite_edit.setValue(self.scenario.facteur_productivite)

        self.risque_edit.setValue(self.scenario.facteur_risque)

        self.disponibilite_edit.setValue(self.scenario.facteur_disponibilite)

        self.actif_check.setChecked(self.scenario.actif)

    def get_scenario(self) -> Scenario:

        if self.scenario:

            self.scenario.nom = self.nom_edit.text().strip()

            self.scenario.description = self.description_edit.toPlainText()

            self.scenario.facteur_productivite = self.productivite_edit.value()

            self.scenario.facteur_risque = self.risque_edit.value()

            self.scenario.facteur_disponibilite = self.disponibilite_edit.value()

            self.scenario.actif = self.actif_check.isChecked()

            return self.scenario

        return Scenario(
            nom=self.nom_edit.text().strip(),
            description=self.description_edit.toPlainText(),
            facteur_productivite=self.productivite_edit.value(),
            facteur_risque=self.risque_edit.value(),
            facteur_disponibilite=self.disponibilite_edit.value(),
            actif=self.actif_check.isChecked(),
        )
