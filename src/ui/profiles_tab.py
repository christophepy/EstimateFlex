from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QAbstractItemView,
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

from src.services.profile_service import ProfileService
from src.ui.profile_dialog import ProfileDialog


class ProfilesTab(QWidget):
    """
    Onglet de gestion des profils utilisateurs.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.profile_service = ProfileService()

        self._build_ui()
        self.load_profiles()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self):

        main_layout = QVBoxLayout(self)

        title = QLabel("Profils utilisateurs")
        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            padding:5px;
            """)

        main_layout.addWidget(title)

        # -----------------------------------------------------
        # Tableau des profils
        # -----------------------------------------------------

        self.profile_table = QTableWidget()
        self.profile_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.profile_table.setColumnCount(10)

        self.profile_table.setHorizontalHeaderLabels(
            [
                "Nom",
                "TJM €",
                "€/h",
                "H/J",
                "Prod",
                "Ligne",
                "Support",
                "Vanne",
                "Bride",
                "Equip.",
            ]
        )

        self.profile_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.profile_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.profile_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.profile_table.verticalHeader().setVisible(False)

        self.profile_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.profile_table.setSortingEnabled(True)
        self.profile_table.setStyleSheet("""
            QTableView::item {
                padding: 2px;
            }

            QTableView::item:selected {
                background-color: #DCEEFF;
                color: black;
            }

            QTableView::item:focus {
                outline: none;
                border: none;
            }
            """)

        main_layout.addWidget(self.profile_table)

        # -----------------------------------------------------
        # Détails du profil
        # -----------------------------------------------------

        self.details_label = QLabel("Sélectionnez un profil.")

        self.details_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.details_label.setWordWrap(True)

        self.details_label.setStyleSheet("""
            background-color:#f5f5f5;
            border:1px solid #d0d0d0;
            padding:10px;
            """)

        self.details_label.setMinimumHeight(130)

        main_layout.addWidget(self.details_label)

        # -----------------------------------------------------
        # Boutons
        # -----------------------------------------------------

        button_layout = QHBoxLayout()

        self.btn_add = QPushButton("Ajouter")
        self.btn_edit = QPushButton("Modifier")
        self.btn_delete = QPushButton("Supprimer")
        self.btn_refresh = QPushButton("Actualiser")

        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_edit)
        button_layout.addWidget(self.btn_delete)

        button_layout.addStretch()

        button_layout.addWidget(self.btn_refresh)

        main_layout.addLayout(button_layout)

        # -----------------------------------------------------
        # Signaux
        # -----------------------------------------------------

        self.btn_add.clicked.connect(self.add_profile)
        self.btn_edit.clicked.connect(self.edit_profile)
        self.btn_delete.clicked.connect(self.delete_profile)
        self.btn_refresh.clicked.connect(self.load_profiles)

        self.profile_table.itemSelectionChanged.connect(self.on_profile_selected)

        self.profile_table.doubleClicked.connect(self.edit_profile)

    # =========================================================
    # Chargement
    # =========================================================

    def load_profiles(self):

        self.profile_table.setSortingEnabled(False)

        selected_profile_id = None

        current = self.get_selected_profile()

        if current:
            selected_profile_id = current.id

        self.profile_table.setRowCount(0)

        try:

            profiles = self.profile_service.get_all_profiles()

            ordre = {
                "Junior": 1,
                "Senior": 2,
                "Expert": 3,
            }

            profiles.sort(key=lambda p: ordre.get(p.nom, 999))

            def centered_item(value):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                return item

            selected_row = None

            for row, profile in enumerate(profiles):

                if profile.id == selected_profile_id:
                    selected_row = row

                self.profile_table.insertRow(row)

                cout_horaire = (
                    profile.taux_journalier / profile.heures_par_jour
                    if profile.heures_par_jour > 0
                    else 0
                )

                item_nom = QTableWidgetItem(profile.nom)

                item_nom.setData(Qt.ItemDataRole.UserRole, profile)

                self.profile_table.setItem(row, 0, item_nom)

                self.profile_table.setItem(
                    row, 1, centered_item(f"{profile.taux_journalier:.0f}")
                )

                self.profile_table.setItem(row, 2, centered_item(f"{cout_horaire:.2f}"))

                self.profile_table.setItem(
                    row, 3, centered_item(f"{profile.heures_par_jour:.1f}")
                )

                item_prod = QTableWidgetItem(f"{profile.facteur_productivite:.2f}")

                item_prod.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                if profile.facteur_productivite > 1.20:

                    item_prod.setBackground(QColor("#C8E6C9"))

                elif profile.facteur_productivite < 0.80:

                    item_prod.setBackground(QColor("#FFF9C4"))

                self.profile_table.setItem(row, 4, item_prod)

                self.profile_table.setItem(
                    row, 5, centered_item(f"{profile.heure_par_ligne:.2f}")
                )

                self.profile_table.setItem(
                    row, 6, centered_item(f"{profile.heure_par_support:.2f}")
                )

                self.profile_table.setItem(
                    row, 7, centered_item(f"{profile.heure_par_vanne:.2f}")
                )

                self.profile_table.setItem(
                    row, 8, centered_item(f"{profile.heure_par_bride:.2f}")
                )

                self.profile_table.setItem(
                    row, 9, centered_item(f"{profile.heure_par_equipement:.2f}")
                )

            if selected_row is not None:

                self.profile_table.selectRow(selected_row)

            elif self.profile_table.rowCount() > 0:

                self.profile_table.selectRow(0)

            else:

                self.details_label.setText("Aucun profil disponible.")

            self.profile_table.setSortingEnabled(True)

        except Exception as exc:

            QMessageBox.critical(
                self, "Erreur", f"Impossible de charger les profils\n\n{exc}"
            )

    # =========================================================
    # Sélection profil
    # =========================================================

    def on_profile_selected(self):

        profile = self.get_selected_profile()

        if profile is None:
            return
        cout_horaire = (
            profile.taux_journalier / profile.heures_par_jour
            if profile.heures_par_jour > 0
            else 0
        )

        self.details_label.setText(f"""
<b>{profile.nom}</b><br><br>

<b>Description :</b><br>
{profile.description or "Aucune description"}<br><br>

<b>Coûts</b><br>
Taux journalier : {profile.taux_journalier:.2f} €/j<br>
Coût horaire : {cout_horaire:.2f} €/h<br>
Heures / jour : {profile.heures_par_jour:.2f}<br>
Facteur productivité : {profile.facteur_productivite:.2f}<br><br>

<b>Paramètres EstimateFlex</b><br>
Temps par ligne : {profile.heure_par_ligne:.2f} h<br>
Temps par support : {profile.heure_par_support:.2f} h<br>
Temps par vanne : {profile.heure_par_vanne:.2f} h<br>
Temps boîte à ressort : {profile.heure_par_boite_a_ressort:.2f} h<br>
Temps compensateur : {profile.heure_compensateur:.2f} h<br>
Temps par bride : {profile.heure_par_bride:.2f} h<br>
Temps par équipement : {profile.heure_par_equipement:.2f} h
""")

    # =========================================================
    # Ajouter
    # =========================================================

    def add_profile(self):

        dialog = ProfileDialog(self)

        if dialog.exec():

            try:

                profile = dialog.get_profile()

                self.profile_service.create_profile(profile)

                self.load_profiles()

            except Exception as exc:

                QMessageBox.critical(self, "Erreur", f"Création impossible\n\n{exc}")

    # =========================================================
    # Modifier
    # =========================================================

    def edit_profile(self):

        profile = self.get_selected_profile()

        if profile is None:

            QMessageBox.warning(self, "Profil", "Veuillez sélectionner un profil.")

            return

        dialog = ProfileDialog(self, profile)

        if dialog.exec():

            try:

                updated_profile = dialog.get_profile()

                self.profile_service.update_profile(updated_profile)

                self.load_profiles()

            except Exception as exc:

                QMessageBox.critical(
                    self, "Erreur", f"Modification impossible\n\n{exc}"
                )

    # =========================================================
    # Suppression
    # =========================================================

    def delete_profile(self):

        profile = self.get_selected_profile()

        if profile is None:

            QMessageBox.warning(self, "Profil", "Veuillez sélectionner un profil.")

            return

        answer = QMessageBox.question(
            self, "Confirmation", f"Supprimer le profil '{profile.nom}' ?"
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:

            self.profile_service.delete_profile(profile.id)

            self.load_profiles()

        except Exception as exc:

            QMessageBox.critical(self, "Erreur", f"Suppression impossible\n\n{exc}")

    # =========================================================
    # Utilitaires
    # =========================================================

    def get_selected_profile(self):

        row = self.profile_table.currentRow()

        if row < 0:
            return None

        item = self.profile_table.item(row, 0)

        if item is None:
            return None

        return item.data(Qt.ItemDataRole.UserRole)

    # =========================================================
    # Refresh
    # =========================================================

    def refresh(self):
        """
        Rafraîchit l'onglet.
        """

        self.load_profiles()
