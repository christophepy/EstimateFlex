from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.services.project_service import ProjectService
from src.ui.project_dialog import ProjectDialog


class ProjectsTab(QWidget):
    """
    Onglet de gestion des projets.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project_service = ProjectService()

        self._build_ui()
        self.load_projects()

    # ==========================================================
    # UI
    # ==========================================================

    def _build_ui(self):

        main_layout = QVBoxLayout(self)

        title = QLabel("Gestion des projets")
        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            padding:6px;
            """)

        main_layout.addWidget(title)

        # --------------------------------------------------
        # Boutons
        # --------------------------------------------------

        button_layout = QHBoxLayout()

        self.btn_new = QPushButton("Nouveau")
        self.btn_edit = QPushButton("Modifier")
        self.btn_delete = QPushButton("Supprimer")
        self.btn_refresh = QPushButton("Actualiser")

        button_layout.addWidget(self.btn_new)
        button_layout.addWidget(self.btn_edit)
        button_layout.addWidget(self.btn_delete)

        button_layout.addStretch()

        button_layout.addWidget(self.btn_refresh)

        main_layout.addLayout(button_layout)

        # --------------------------------------------------
        # Tableau
        # --------------------------------------------------

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

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels(
            [
                "Nom",
                "Client",
                "Lignes",
                "Supports",
                "Composants",
                "Livrables Calcul",
                "Livrables Plans",
            ]
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setSortingEnabled(True)

        main_layout.addWidget(self.table)

        # --------------------------------------------------
        # Détail projet
        # --------------------------------------------------

        self.details_label = QLabel("Sélectionnez un projet.")

        self.details_label.setWordWrap(True)

        self.details_label.setMinimumHeight(250)

        self.details_label.setStyleSheet("""
            background-color:#f5f5f5;
            border:1px solid #d0d0d0;
            padding:10px;
            """)

        main_layout.addWidget(self.details_label)

        # --------------------------------------------------
        # Signaux
        # --------------------------------------------------

        self.btn_new.clicked.connect(self.create_project)

        self.btn_edit.clicked.connect(self.edit_project)

        self.btn_delete.clicked.connect(self.delete_project)

        self.btn_refresh.clicked.connect(self.load_projects)

        self.table.doubleClicked.connect(self.edit_project)

        self.table.itemSelectionChanged.connect(self.on_project_selected)

    # ==========================================================
    # Chargement
    # ==========================================================

    def load_projects(self):

        try:

            projects = self.project_service.get_all_projects()

            self.table.setRowCount(len(projects))

            for row, project in enumerate(projects):

                composants = (
                    project.parameters.nb_vannes
                    + project.parameters.nb_brides
                    + project.parameters.nb_compensateur
                    + project.parameters.nb_connexions_equipements
                    + project.parameters.nb_soudures
                )

                livrables_calcul = (
                    project.deliverables.rapport_calcul
                    + project.deliverables.rapport_calcul_intermediare
                    + project.deliverables.fichier_resultat
                )

                livrables_plans = (
                    project.deliverables.notes_supports
                    + project.deliverables.notes_equipements
                    + project.deliverables.plans_supports
                    + project.deliverables.presentation_client
                    + project.deliverables.fichier_modele
                )

                self.table.setItem(
                    row,
                    0,
                    QTableWidgetItem(project.nom),
                )

                self.table.setItem(
                    row,
                    1,
                    QTableWidgetItem(project.client),
                )

                self.table.setItem(
                    row,
                    2,
                    QTableWidgetItem(str(project.parameters.nb_lignes)),
                )

                self.table.setItem(
                    row,
                    3,
                    QTableWidgetItem(str(project.parameters.nb_supports)),
                )

                self.table.setItem(
                    row,
                    4,
                    QTableWidgetItem(str(composants)),
                )

                self.table.setItem(
                    row,
                    5,
                    QTableWidgetItem(str(livrables_calcul)),
                )

                self.table.setItem(
                    row,
                    6,
                    QTableWidgetItem(str(livrables_plans)),
                )

            if self.table.rowCount() > 0:
                self.table.selectRow(0)

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Erreur",
                f"Impossible de charger les projets\n\n{exc}",
            )

    # ==========================================================
    # Helpers
    # ==========================================================

    def get_selected_project(self):

        row = self.table.currentRow()

        if row < 0:
            return None

        item = self.table.item(row, 0)

        if item is None:
            return None

        return self.project_service.get_project_by_nom(item.text())

    # ==========================================================
    # CRUD
    # ==========================================================

    def create_project(self):

        dialog = ProjectDialog(parent=self)

        if dialog.exec():

            project = dialog.get_project()

            self.project_service.create_project(project)

            self.load_projects()

    def edit_project(self):

        project = self.get_selected_project()

        if project is None:

            QMessageBox.warning(
                self,
                "Projet",
                "Sélectionnez un projet.",
            )

            return

        dialog = ProjectDialog(
            project=project,
            parent=self,
        )

        if dialog.exec():

            self.project_service.update_project(
                dialog.get_project(),
            )

            self.load_projects()

    def delete_project(self):

        project = self.get_selected_project()

        if project is None:

            QMessageBox.warning(
                self,
                "Projet",
                "Sélectionnez un projet.",
            )

            return

        answer = QMessageBox.question(
            self,
            "Confirmation",
            f"Supprimer '{project.nom}' ?",
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:

            self.project_service.delete_project(project.nom)

            self.load_projects()

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Erreur",
                str(exc),
            )

    def on_project_selected(self):

        project = self.get_selected_project()

        if project is None:
            return

        self.details_label.setText(f"""
    <b>{project.nom}</b><br><br>

    <b>Client</b><br>
    {project.client}<br><br>

    <b>Description</b><br>
    {project.description}<br><br>

    <b>Paramètres techniques</b><br>
    Lignes : {project.parameters.nb_lignes}<br>
    Supports : {project.parameters.nb_supports}<br>
    Vannes : {project.parameters.nb_vannes}<br>
    Brides : {project.parameters.nb_brides}<br>
    Compensateurs : {project.parameters.nb_compensateur}<br>
    Connexions équipements : {project.parameters.nb_connexions_equipements}<br>
    Soudures : {project.parameters.nb_soudures}<br><br>

    <b>Livrables Calcul</b><br>
    Rapports calcul : {project.deliverables.rapport_calcul}<br>
    Rapports intermédiaires : {project.deliverables.rapport_calcul_intermediare}<br>
    Fichiers résultats : {project.deliverables.fichier_resultat}<br><br>

    <b>Livrables Plans</b><br>
    Notes supports : {project.deliverables.notes_supports}<br>
    Notes équipements : {project.deliverables.notes_equipements}<br>
    Plans supports : {project.deliverables.plans_supports}<br>
    Présentation client : {project.deliverables.presentation_client}<br>
    Fichier modèle : {project.deliverables.fichier_modele}<br><br>

    <b>Revues</b><br>
    Revues internes : {project.reviews.nb_revues_internes}<br>
    Revues client : {project.reviews.nb_revues_client}<br>
    Allers-retours : {project.reviews.nb_aller_retour}
    """)

    # =========================================================
    # Refresh
    # =========================================================

    def refresh(self):
        """
        Rafraîchit l'onglet.
        """

        self.load_projects()
