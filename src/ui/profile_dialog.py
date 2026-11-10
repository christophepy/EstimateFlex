# src/ui/profile_dialog.py

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
)

from src.models.user_profile import UserProfile


class ProfileDialog(QDialog):

    def __init__(self, parent=None, profile=None):
        super().__init__(parent)

        self.profile = profile

        self.setWindowTitle("Profil utilisateur")
        self.resize(600, 700)

        self._build_ui()
        self._load_profile()

    def _build_ui(self):

        layout = QVBoxLayout(self)

        # -----------------------------
        # Informations générales
        # -----------------------------

        info_group = QGroupBox("Informations")
        info_form = QFormLayout()

        self.nom_edit = QLineEdit()

        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)

        info_form.addRow("Nom :", self.nom_edit)
        info_form.addRow("Description :", self.description_edit)

        info_group.setLayout(info_form)

        # -----------------------------
        # Coûts
        # -----------------------------

        cout_group = QGroupBox("Coûts")

        cout_form = QFormLayout()

        self.taux_journalier_edit = QDoubleSpinBox()
        self.taux_journalier_edit.setRange(0, 10000)
        self.taux_journalier_edit.setDecimals(2)
        self.taux_journalier_edit.setSuffix(" €/j")

        self.heures_par_jour_edit = QDoubleSpinBox()
        self.heures_par_jour_edit.setRange(1, 24)
        self.heures_par_jour_edit.setDecimals(2)

        self.heures_par_jour_edit.setValue(7.0)

        self.facteur_productivite_edit = QDoubleSpinBox()
        self.facteur_productivite_edit.setRange(0.1, 5.0)
        self.facteur_productivite_edit.setDecimals(2)
        self.facteur_productivite_edit.setSingleStep(0.05)
        self.facteur_productivite_edit.setValue(1.0)

        cout_form.addRow("Taux journalier :", self.taux_journalier_edit)

        cout_form.addRow("Heures / jour :", self.heures_par_jour_edit)

        cout_form.addRow("Facteur productivité :", self.facteur_productivite_edit)

        cout_group.setLayout(cout_form)

        # -----------------------------
        # Paramètres EstimateFlex
        # -----------------------------

        param_group = QGroupBox("Paramètres d'estimation")

        param_form = QFormLayout()

        self.heure_par_ligne_edit = self._create_time_spin()
        self.heure_par_support_edit = self._create_time_spin()
        self.heure_par_vanne_edit = self._create_time_spin()
        self.heure_par_boite_a_ressort_edit = self._create_time_spin()
        self.heure_compensateur_edit = self._create_time_spin()
        self.heure_par_bride_edit = self._create_time_spin()
        self.heure_par_equipement_edit = self._create_time_spin()

        param_form.addRow("Temps par ligne :", self.heure_par_ligne_edit)

        param_form.addRow("Temps par support :", self.heure_par_support_edit)

        param_form.addRow("Temps par vanne :", self.heure_par_vanne_edit)

        param_form.addRow(
            "Temps par boîte à ressort :", self.heure_par_boite_a_ressort_edit
        )

        param_form.addRow("Temps compensateur :", self.heure_compensateur_edit)

        param_form.addRow("Temps par bride :", self.heure_par_bride_edit)

        param_form.addRow("Temps par équipement :", self.heure_par_equipement_edit)

        param_group.setLayout(param_form)

        # -----------------------------
        # Boutons
        # -----------------------------

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # -----------------------------
        # Layout principal
        # -----------------------------

        layout.addWidget(info_group)
        layout.addWidget(cout_group)
        layout.addWidget(param_group)
        layout.addWidget(buttons)

    def _create_time_spin(self):

        spin = QDoubleSpinBox()

        spin.setRange(0.0, 20.0)
        spin.setDecimals(2)
        spin.setSingleStep(0.05)

        return spin

    def _load_profile(self):

        if not self.profile:
            return

        self.nom_edit.setText(self.profile.nom)

        self.description_edit.setPlainText(self.profile.description)

        self.taux_journalier_edit.setValue(self.profile.taux_journalier)

        self.heures_par_jour_edit.setValue(self.profile.heures_par_jour)

        self.facteur_productivite_edit.setValue(self.profile.facteur_productivite)

        self.heure_par_ligne_edit.setValue(self.profile.heure_par_ligne)

        self.heure_par_support_edit.setValue(self.profile.heure_par_support)

        self.heure_par_vanne_edit.setValue(self.profile.heure_par_vanne)

        self.heure_par_boite_a_ressort_edit.setValue(
            self.profile.heure_par_boite_a_ressort
        )

        self.heure_compensateur_edit.setValue(self.profile.heure_compensateur)

        self.heure_par_bride_edit.setValue(self.profile.heure_par_bride)

        self.heure_par_equipement_edit.setValue(self.profile.heure_par_equipement)

    def get_profile(self) -> UserProfile:

        if self.profile:

            self.profile.nom = self.nom_edit.text().strip()

            self.profile.description = self.description_edit.toPlainText()

            self.profile.taux_journalier = self.taux_journalier_edit.value()

            self.profile.heures_par_jour = self.heures_par_jour_edit.value()

            self.profile.facteur_productivite = self.facteur_productivite_edit.value()

            self.profile.heure_par_ligne = self.heure_par_ligne_edit.value()

            self.profile.heure_par_support = self.heure_par_support_edit.value()

            self.profile.heure_par_vanne = self.heure_par_vanne_edit.value()

            self.profile.heure_par_boite_a_ressort = (
                self.heure_par_boite_a_ressort_edit.value()
            )

            self.profile.heure_compensateur = self.heure_compensateur_edit.value()

            self.profile.heure_par_bride = self.heure_par_bride_edit.value()

            self.profile.heure_par_equipement = self.heure_par_equipement_edit.value()

            return self.profile

        return UserProfile(
            nom=self.nom_edit.text().strip(),
            description=self.description_edit.toPlainText(),
            taux_journalier=self.taux_journalier_edit.value(),
            heures_par_jour=self.heures_par_jour_edit.value(),
            facteur_productivite=self.facteur_productivite_edit.value(),
            heure_par_ligne=self.heure_par_ligne_edit.value(),
            heure_par_support=self.heure_par_support_edit.value(),
            heure_par_vanne=self.heure_par_vanne_edit.value(),
            heure_par_boite_a_ressort=self.heure_par_boite_a_ressort_edit.value(),
            heure_compensateur=self.heure_compensateur_edit.value(),
            heure_par_bride=self.heure_par_bride_edit.value(),
            heure_par_equipement=self.heure_par_equipement_edit.value(),
        )
