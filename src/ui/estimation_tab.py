# src/ui/estimation_tab.py

from PyQt6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.services.estimation_service import EstimationService
from src.services.profile_service import ProfileService
from src.services.project_service import ProjectService
from src.services.scenario_service import ScenarioService


class EstimationTab(QWidget):
    """
    Onglet d'estimation principal.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.estimation_service = EstimationService()
        self.profile_service = ProfileService()
        self.project_service = ProjectService()
        self.scenario_service = ScenarioService()

        self._build_ui()
        self._load_data()

    def _build_ui(self):

        main_layout = QVBoxLayout(self)

        # =====================================================
        # PARAMETRES
        # =====================================================

        parameters_group = QGroupBox("Paramètres d'estimation")
        parameters_layout = QGridLayout()

        self.profile_combo = QComboBox()
        self.project_combo = QComboBox()
        self.scenario_combo = QComboBox()

        self.scenario_combo.clear()

        for scenario in self.scenario_service.get_all_scenarios():
            self.scenario_combo.addItem(
                scenario.nom,
                scenario,
            )

        parameters_layout.addWidget(QLabel("Profil :"), 0, 0)
        parameters_layout.addWidget(self.profile_combo, 0, 1)

        parameters_layout.addWidget(QLabel("Projet :"), 1, 0)
        parameters_layout.addWidget(self.project_combo, 1, 1)

        parameters_layout.addWidget(QLabel("Scénario :"), 2, 0)
        parameters_layout.addWidget(self.scenario_combo, 2, 1)

        parameters_group.setLayout(parameters_layout)

        # =====================================================
        # BOUTON
        # =====================================================

        button_layout = QHBoxLayout()

        self.estimate_button = QPushButton("Calculer l'estimation")
        self.estimate_button.clicked.connect(self.calculate_estimation)

        button_layout.addStretch()
        button_layout.addWidget(self.estimate_button)

        # =====================================================
        # RESULTATS
        # =====================================================

        results_group = QGroupBox("Résultats")

        results_layout = QGridLayout()

        self.hours_edit = QLineEdit()
        self.days_edit = QLineEdit()
        self.cost_edit = QLineEdit()

        for widget in [
            self.hours_edit,
            self.days_edit,
            self.cost_edit,
        ]:
            widget.setReadOnly(True)

        results_layout.addWidget(QLabel("Heures estimées"), 0, 0)
        results_layout.addWidget(self.hours_edit, 0, 1)

        results_layout.addWidget(QLabel("Jours estimés"), 1, 0)
        results_layout.addWidget(self.days_edit, 1, 1)

        results_layout.addWidget(QLabel("Coût estimé (€)"), 2, 0)
        results_layout.addWidget(self.cost_edit, 2, 1)

        results_group.setLayout(results_layout)

        # =====================================================
        # DETAILS
        # =====================================================

        details_group = QGroupBox("Détails du calcul")

        details_layout = QVBoxLayout()

        self.details_text = QTextEdit()

        self.details_text.setReadOnly(True)

        # Hauteur fixe pour afficher
        # toutes les informations sans scroll
        self.details_text.setFixedHeight(350)

        details_layout.addWidget(self.details_text)

        details_group.setLayout(details_layout)

        # =====================================================
        # ASSEMBLAGE
        # =====================================================

        main_layout.addWidget(parameters_group)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(results_group)
        main_layout.addWidget(details_group)

        main_layout.addStretch()

    def _load_data(self):
        """
        Charge profils, projets et scénarios.
        """

        self.profile_combo.clear()
        self.project_combo.clear()
        self.scenario_combo.clear()

        try:

            profiles = self.profile_service.get_all_profiles()

            for profile in profiles:

                self.profile_combo.addItem(
                    profile.nom,
                    profile,
                )

        except Exception as exc:

            print(f"Erreur chargement profils : {exc}")

        try:

            projects = self.project_service.get_all_projects()

            for project in projects:

                self.project_combo.addItem(
                    project.nom,
                    project,
                )

        except Exception as exc:

            print(f"Erreur chargement projets : {exc}")

        try:

            scenarios = self.scenario_service.get_all_scenarios()

            for scenario in scenarios:

                self.scenario_combo.addItem(
                    scenario.nom,
                    scenario,
                )

        except Exception as exc:

            print(f"Erreur chargement scénarios : {exc}")

    def calculate_estimation(self):

        try:

            profile = self.profile_combo.currentData()
            project = self.project_combo.currentData()
            scenario = self.scenario_combo.currentData()

            if profile is None:
                QMessageBox.warning(
                    self, "Profil manquant", "Veuillez sélectionner un profil."
                )
                return

            if project is None:
                QMessageBox.warning(
                    self, "Projet manquant", "Veuillez sélectionner un projet."
                )
                return

            if scenario is None:
                QMessageBox.warning(
                    self, "Scénario manquant", "Veuillez sélectionner un scénario."
                )

                return

            result = self.estimation_service.estimate(
                project=project,
                profile=profile,
                scenario=scenario,
            )

            self.hours_edit.setText(f"{result.estimated_hours:.2f}")

            self.days_edit.setText(f"{result.estimated_days:.2f}")

            self.cost_edit.setText(f"{result.estimated_cost:,.2f}")

            self._display_details(
                project,
                profile,
                scenario,
                result,
            )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Erreur",
                str(exc),
            )
        # rechzechz erreur
        print(profile.nom)
        print(profile.facteur_productivite)
        # ++

    def _display_details(
        self,
        project,
        profile,
        scenario,
        result,
    ):

        details = []

        details.append("===== CONTEXTE =====")

        details.append(f"Projet : {project.nom}")

        details.append(f"Profil : {profile.nom}")

        details.append(f"Scénario : {scenario.nom}")

        details.append("")

        details.append("===== PARAMÈTRES DU SCÉNARIO =====")

        details.append(f"Description : {scenario.description}")

        details.append(f"Facteur productivité : {scenario.facteur_productivite:.2f}")

        details.append(f"Facteur risque : {scenario.facteur_risque:.2f}")

        details.append(f"Facteur disponibilité : {scenario.facteur_disponibilite:.2f}")

        details.append("")

        details.append("===== RÉSULTATS =====")

        details.append(f"Heures estimées : {result.estimated_hours:.2f}")

        details.append(f"Jours estimés : {result.estimated_days:.2f}")

        details.append(
            f"Coût estimé : {result.estimated_cost:,.2f}".replace(",", " ") + " €"
        )

        self.details_text.setPlainText("\n".join(details))

    def refresh(self):
        """
        Rafraîchit les données de l'onglet.
        """
        self._load_data()
