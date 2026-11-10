from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
)

from src.models.deliverables import Deliverables
from src.models.project import Project
from src.models.project_parameters import ProjectParameters
from src.models.review_metrics import ReviewMetrics


class ProjectDialog(QDialog):
    """
    Dialogue de création / modification projet.
    """

    def __init__(
        self,
        project=None,
        parent=None,
    ):
        super().__init__(parent)

        self.project = project

        self.setWindowTitle("Projet")
        self.resize(800, 900)

        self._build_ui()
        self._load_project()

    def _build_ui(self):

        layout = QVBoxLayout(self)

        # --------------------------------------------------
        # Informations
        # --------------------------------------------------

        info_group = QGroupBox("Informations générales")

        info_form = QFormLayout()

        self.nom_edit = QLineEdit()

        self.client_edit = QLineEdit()

        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)

        info_form.addRow(
            "Nom :",
            self.nom_edit,
        )

        info_form.addRow(
            "Client :",
            self.client_edit,
        )

        info_form.addRow(
            "Description :",
            self.description_edit,
        )

        info_group.setLayout(info_form)

        # --------------------------------------------------
        # Paramètres techniques
        # --------------------------------------------------

        param_group = QGroupBox("Paramètres techniques")

        param_form = QFormLayout()

        self.nb_lignes_edit = QSpinBox()
        self.nb_supports_edit = QSpinBox()
        self.nb_vannes_edit = QSpinBox()
        self.nb_brides_edit = QSpinBox()
        self.nb_compensateur_edit = QSpinBox()
        self.nb_connexions_edit = QSpinBox()
        self.nb_soudures_edit = QSpinBox()

        for spin in (
            self.nb_lignes_edit,
            self.nb_supports_edit,
            self.nb_vannes_edit,
            self.nb_brides_edit,
            self.nb_compensateur_edit,
            self.nb_connexions_edit,
            self.nb_soudures_edit,
        ):
            spin.setRange(0, 100000)

        param_form.addRow(
            "Lignes :",
            self.nb_lignes_edit,
        )

        param_form.addRow(
            "Supports :",
            self.nb_supports_edit,
        )

        param_form.addRow(
            "Vannes :",
            self.nb_vannes_edit,
        )

        param_form.addRow(
            "Brides :",
            self.nb_brides_edit,
        )

        param_form.addRow(
            "Compensateurs :",
            self.nb_compensateur_edit,
        )

        param_form.addRow(
            "Connexions équipements :",
            self.nb_connexions_edit,
        )

        param_form.addRow(
            "Soudures :",
            self.nb_soudures_edit,
        )

        param_group.setLayout(param_form)

        # --------------------------------------------------
        # Livrables
        # --------------------------------------------------

        livrable_group = QGroupBox("Livrables")

        livrable_form = QFormLayout()

        self.rapport_calcul_edit = QSpinBox()
        self.rapport_inter_edit = QSpinBox()
        self.notes_supports_edit = QSpinBox()
        self.notes_equipements_edit = QSpinBox()
        self.plans_supports_edit = QSpinBox()
        self.presentation_client_edit = QSpinBox()
        self.fichier_modele_edit = QSpinBox()
        self.fichier_resultat_edit = QSpinBox()

        livrable_form.addRow(
            "Rapport calcul :",
            self.rapport_calcul_edit,
        )

        livrable_form.addRow(
            "Rapport intermédiaire :",
            self.rapport_inter_edit,
        )

        livrable_form.addRow(
            "Notes supports :",
            self.notes_supports_edit,
        )

        livrable_form.addRow(
            "Notes équipements :",
            self.notes_equipements_edit,
        )

        livrable_form.addRow(
            "Plans supports :",
            self.plans_supports_edit,
        )

        livrable_form.addRow(
            "Présentation client :",
            self.presentation_client_edit,
        )

        livrable_form.addRow(
            "Fichier modèle :",
            self.fichier_modele_edit,
        )

        livrable_form.addRow(
            "Fichier résultat :",
            self.fichier_resultat_edit,
        )

        livrable_group.setLayout(livrable_form)

        # --------------------------------------------------
        # Revues
        # --------------------------------------------------

        review_group = QGroupBox("Revues")

        review_form = QFormLayout()

        self.revues_internes_edit = QSpinBox()
        self.revues_client_edit = QSpinBox()
        self.aller_retour_edit = QSpinBox()

        review_form.addRow(
            "Revues internes :",
            self.revues_internes_edit,
        )

        review_form.addRow(
            "Revues client :",
            self.revues_client_edit,
        )

        review_form.addRow(
            "Allers-retours :",
            self.aller_retour_edit,
        )

        review_group.setLayout(review_form)

        # --------------------------------------------------
        # Boutons
        # --------------------------------------------------

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)

        buttons.rejected.connect(self.reject)

        layout.addWidget(info_group)
        layout.addWidget(param_group)
        layout.addWidget(livrable_group)
        layout.addWidget(review_group)
        layout.addWidget(buttons)

    def _load_project(self):

        if self.project is None:
            return

        self.nom_edit.setText(self.project.nom)

        self.client_edit.setText(self.project.client)

        self.description_edit.setPlainText(self.project.description)

        self.nb_lignes_edit.setValue(self.project.parameters.nb_lignes)

        self.nb_supports_edit.setValue(self.project.parameters.nb_supports)

        self.nb_vannes_edit.setValue(self.project.parameters.nb_vannes)

        self.nb_brides_edit.setValue(self.project.parameters.nb_brides)

        self.nb_compensateur_edit.setValue(self.project.parameters.nb_compensateur)

        self.nb_connexions_edit.setValue(
            self.project.parameters.nb_connexions_equipements
        )

        self.nb_soudures_edit.setValue(self.project.parameters.nb_soudures)

        self.rapport_calcul_edit.setValue(self.project.deliverables.rapport_calcul)

        self.rapport_inter_edit.setValue(
            self.project.deliverables.rapport_calcul_intermediare
        )

        self.notes_supports_edit.setValue(self.project.deliverables.notes_supports)

        self.notes_equipements_edit.setValue(
            self.project.deliverables.notes_equipements
        )

        self.plans_supports_edit.setValue(self.project.deliverables.plans_supports)

        self.presentation_client_edit.setValue(
            self.project.deliverables.presentation_client
        )

        self.fichier_modele_edit.setValue(self.project.deliverables.fichier_modele)

        self.fichier_resultat_edit.setValue(self.project.deliverables.fichier_resultat)

        self.revues_internes_edit.setValue(self.project.reviews.nb_revues_internes)

        self.revues_client_edit.setValue(self.project.reviews.nb_revues_client)

        self.aller_retour_edit.setValue(self.project.reviews.nb_aller_retour)

    def get_project(self):

        parameters = ProjectParameters(
            nb_lignes=self.nb_lignes_edit.value(),
            nb_supports=self.nb_supports_edit.value(),
            nb_vannes=self.nb_vannes_edit.value(),
            nb_brides=self.nb_brides_edit.value(),
            nb_compensateur=self.nb_compensateur_edit.value(),
            nb_connexions_equipements=self.nb_connexions_edit.value(),
            nb_soudures=self.nb_soudures_edit.value(),
        )

        deliverables = Deliverables(
            rapport_calcul=self.rapport_calcul_edit.value(),
            rapport_calcul_intermediare=self.rapport_inter_edit.value(),
            notes_supports=self.notes_supports_edit.value(),
            notes_equipements=self.notes_equipements_edit.value(),
            plans_supports=self.plans_supports_edit.value(),
            presentation_client=self.presentation_client_edit.value(),
            fichier_modele=self.fichier_modele_edit.value(),
            fichier_resultat=self.fichier_resultat_edit.value(),
        )

        reviews = ReviewMetrics(
            nb_revues_internes=self.revues_internes_edit.value(),
            nb_revues_client=self.revues_client_edit.value(),
            nb_aller_retour=self.aller_retour_edit.value(),
        )

        if self.project is not None:

            self.project.nom = self.nom_edit.text().strip()
            self.project.client = self.client_edit.text().strip()
            self.project.description = self.description_edit.toPlainText()

            self.project.parameters = parameters
            self.project.deliverables = deliverables
            self.project.reviews = reviews

            return self.project

        return Project(
            nom=self.nom_edit.text().strip(),
            client=self.client_edit.text().strip(),
            description=self.description_edit.toPlainText(),
            parameters=parameters,
            deliverables=deliverables,
            reviews=reviews,
        )
