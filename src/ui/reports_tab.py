# reports_tab.py
import copy
import os
import subprocess
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.services.excel_export_service import ExcelExportService
from src.services.pdf_export_service import PdfExportService
from src.utils.formatters import (
    format_currency,
    format_number,
)


class NumericTableWidgetItem(QTableWidgetItem):

    def __lt__(self, other):

        try:
            return float(self.data(Qt.ItemDataRole.UserRole)) < float(
                other.data(Qt.ItemDataRole.UserRole)
            )
        except Exception:
            return super().__lt__(other)


class ReportsTab(QWidget):

    def __init__(
        self,
        estimation_repository,
        settings_service,
        currency_service,
        parent=None,
    ):
        super().__init__(parent)

        self.estimation_repository = estimation_repository

        self.settings_service = settings_service
        self.settings = self.settings_service.get()
        self.currency_service = currency_service

        self.estimation_repository = estimation_repository
        self.pdf_export_service = PdfExportService()
        self.excel_export_service = ExcelExportService()
        self._build_ui()
        self.load_reports()

    # =====================================================================
    # UI
    # =====================================================================

    def _build_ui(self):

        main_layout = QVBoxLayout(self)

        # ---------------------------------------------------------
        # Tableau
        # ---------------------------------------------------------

        self.reports_table = QTableWidget()

        self.reports_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.reports_table.setStyleSheet("""
            QTableView::item:focus {
                outline: none;
                border: none;
        }
        """)

        self.reports_table.setColumnCount(8)

        self.reports_table.setHorizontalHeaderLabels(
            [
                "Nom",
                "Projet",
                "Scénario",
                "Heures",
                "Jours",
                "Coût",
                "Risque",
                "Date",
            ]
        )

        self.reports_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.reports_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.reports_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.reports_table.setStyleSheet("""
            QTableView::item:selected {
                background-color: #DCEEFF;
                color: black;
            }

            QTableView::item:focus {
            outline: none;
            border: none;
            }
        """)

        self.reports_table.setSortingEnabled(True)

        self.reports_table.horizontalHeader().setStretchLastSection(True)

        self.reports_table.itemSelectionChanged.connect(self._update_details)

        self.reports_table.itemDoubleClicked.connect(self._open_report)

        main_layout.addWidget(self.reports_table)

        # ---------------------------------------------------------
        # Boutons
        # ---------------------------------------------------------

        buttons_layout = QHBoxLayout()

        self.open_btn = QPushButton("Ouvrir")
        self.rename_btn = QPushButton("Renommer")
        self.delete_btn = QPushButton("Supprimer")
        self.refresh_btn = QPushButton("Actualiser")
        self.open_exports_btn = QPushButton("Ouvrir exports")
        self.pdf_btn = QPushButton("Exporter PDF")
        self.excel_btn = QPushButton("Exporter Excel")

        self.open_btn.clicked.connect(self._open_report)
        self.rename_btn.clicked.connect(self.rename_report)
        self.delete_btn.clicked.connect(self.delete_report)
        self.refresh_btn.clicked.connect(self.load_reports)
        self.open_exports_btn.clicked.connect(self.open_exports_folder)
        self.pdf_btn.clicked.connect(self.export_pdf)
        self.excel_btn.clicked.connect(self.export_excel)

        buttons_layout.addWidget(self.open_btn)
        buttons_layout.addWidget(self.rename_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addWidget(self.pdf_btn)
        buttons_layout.addWidget(self.excel_btn)
        buttons_layout.addWidget(self.open_exports_btn)
        buttons_layout.addWidget(self.refresh_btn)
        buttons_layout.addStretch()

        main_layout.addLayout(buttons_layout)

        # ---------------------------------------------------------
        # Détail
        # ---------------------------------------------------------

        details_group = QGroupBox("Détail estimation")

        form = QFormLayout()

        self.lbl_name = QLabel("-")
        self.lbl_project = QLabel("-")
        self.lbl_scenario = QLabel("-")
        self.lbl_budget = QLabel("-")
        self.lbl_date = QLabel("-")

        form.addRow("Nom :", self.lbl_name)
        form.addRow("Projet :", self.lbl_project)
        form.addRow("Scénario :", self.lbl_scenario)
        form.addRow("Budget :", self.lbl_budget)
        form.addRow("Date :", self.lbl_date)

        details_group.setLayout(form)

        main_layout.addWidget(details_group)

    # =====================================================================
    # Chargement
    # =====================================================================

    def load_reports(self):

        self.settings = self.settings_service.get()

        self.reports_table.setRowCount(0)
        self.reports_table.setCurrentCell(-1, -1)

        if self.estimation_repository is None:
            return

        try:

            reports = self.estimation_repository.get_all()

            self.reports_table.setSortingEnabled(False)
            self.reports_table.setRowCount(len(reports))

            for row, report in enumerate(reports):

                item = QTableWidgetItem(str(report.estimation_nom))
                item.setData(Qt.ItemDataRole.UserRole, report.id)

                self.reports_table.setItem(row, 0, item)

                self.reports_table.setItem(
                    row,
                    1,
                    QTableWidgetItem(str(report.project_nom)),
                )

                self.reports_table.setItem(
                    row,
                    2,
                    QTableWidgetItem(str(report.scenario_nom)),
                )

                hours_item = NumericTableWidgetItem(
                    format_number(report.estimated_hours)
                )

                hours_item.setData(
                    Qt.ItemDataRole.UserRole,
                    report.estimated_hours,
                )

                self.reports_table.setItem(
                    row,
                    3,
                    hours_item,
                )

                days_item = NumericTableWidgetItem(format_number(report.estimated_days))

                days_item.setData(
                    Qt.ItemDataRole.UserRole,
                    report.estimated_days,
                )

                self.reports_table.setItem(
                    row,
                    4,
                    days_item,
                )

                display_cost = self.currency_service.convert(
                    report.estimated_cost,
                    self.settings.currency,
                )

                cost_item = NumericTableWidgetItem(format_number(display_cost))

                cost_item.setData(
                    Qt.ItemDataRole.UserRole,
                    display_cost,
                )

                self.reports_table.setItem(
                    row,
                    5,
                    cost_item,
                )

                risk_item = NumericTableWidgetItem(format_number(report.risk_factor))

                risk_item.setData(
                    Qt.ItemDataRole.UserRole,
                    report.risk_factor,
                )

                self.reports_table.setItem(
                    row,
                    6,
                    risk_item,
                )

                self.reports_table.setItem(
                    row,
                    7,
                    QTableWidgetItem(str(report.created_at)),
                )

            self.reports_table.resizeColumnsToContents()
            self.reports_table.setSortingEnabled(True)

        except Exception as exc:

            QMessageBox.warning(
                self,
                "Reports",
                f"Impossible de charger les rapports :\n{exc}",
            )

    # =====================================================================
    # Sélection
    # =====================================================================

    def _get_selected_report(self):

        if self.estimation_repository is None:
            return None

        row = self.reports_table.currentRow()

        if row < 0:
            return None

        item = self.reports_table.item(row, 0)

        if item is None:
            return None

        estimation_id = item.data(Qt.ItemDataRole.UserRole)

        if estimation_id is None:
            return None

        return self.estimation_repository.get_estimation(estimation_id)

    # =====================================================================
    # Détail
    # =====================================================================

    def _update_details(self):

        report = self._get_selected_report()

        if report is None:
            return

        self.settings = self.settings_service.get()

        display_cost = self.currency_service.convert(
            report.estimated_cost,
            self.settings.currency,
        )

        self.lbl_name.setText(str(report.estimation_nom))

        self.lbl_project.setText(str(report.project_nom))

        self.lbl_scenario.setText(str(report.scenario_nom))

        self.lbl_budget.setText(
            f"{format_number(report.estimated_hours)} h | "
            f"{format_number(report.estimated_days)} j | "
            f"{format_currency(display_cost, self.settings.currency)}"
        )

        self.lbl_date.setText(
            f"Risque : {format_number(report.risk_factor)} | " f"{report.created_at}"
        )

    # =====================================================================
    # Ouvrir
    # =====================================================================

    def _open_report(self):

        report = self._get_selected_report()

        if report is None:
            return

        QMessageBox.information(
            self,
            "Détail estimation",
            (
                f"Nom : {report.estimation_nom}\n\n"
                f"Projet : {report.project_nom}\n"
                f"Scénario : {report.scenario_nom}\n\n"
                f"Heures : {format_number(report.estimated_hours)}\n"
                f"Jours : {format_number(report.estimated_days)}\n"
                f"Coût : "
                f"{format_currency(report.estimated_cost, self.settings.currency)}\n"
                f"Risque : {format_number(report.risk_factor)}\n\n"
                f"Créée le :\n"
                f"{report.created_at}"
            ),
        )

    # =====================================================================
    # Renommer
    # =====================================================================

    def rename_report(self):

        report = self._get_selected_report()

        if report is None:
            return

        new_name, ok = QInputDialog.getText(
            self,
            "Renommer estimation",
            "Nouveau nom :",
            text=report.estimation_nom,
        )

        if not ok:
            return

        new_name = new_name.strip()

        if not new_name:
            return

        self.estimation_repository.rename_estimation(
            report.id,
            new_name,
        )

        self.load_reports()

    # =====================================================================
    # Supprimer
    # =====================================================================

    def delete_report(self):

        report = self._get_selected_report()

        if report is None:
            return

        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Supprimer l'estimation\n\n{report.estimation_nom} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        self.estimation_repository.delete_estimation(report.id)

        self.load_reports()

    # =====================================================================
    # Export pdf
    # =====================================================================

    def export_pdf(self):

        report = self._get_selected_report()

        if report is None:

            QMessageBox.warning(self, "Export PDF", "Sélectionnez une estimation.")

            return

        try:

            settings = self.settings_service.get()

            base_dir = Path(settings.export_directory)

            export_dir = base_dir / "pdf"

            export_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            file_path = export_dir / f"{report.estimation_nom}.pdf"

            report_export = copy.copy(report)

            report_export.estimated_cost = self.currency_service.convert(
                report.estimated_cost,
                settings.currency,
            )

            output = PdfExportService.export(
                report_export,
                str(file_path),
                settings.currency,
            )

            QMessageBox.information(
                self,
                "Export PDF",
                f"PDF exporté :\n\n{output}",
            )

        except Exception as exc:

            QMessageBox.critical(self, "Erreur Export PDF", str(exc))

    # =====================================================================
    # Export Excel
    # =====================================================================

    def export_excel(self):

        report = self._get_selected_report()

        if report is None:

            QMessageBox.warning(self, "Export Excel", "Sélectionnez une estimation.")

            return

        try:

            settings = self.settings_service.get()

            base_dir = Path(settings.export_directory)

            export_dir = base_dir / "excel"

            export_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            file_path = export_dir / f"{report.estimation_nom}.xlsx"

            report_export = copy.copy(report)

            report_export.estimated_cost = self.currency_service.convert(
                report.estimated_cost,
                settings.currency,
            )

            output = ExcelExportService.export(
                report_export,
                str(file_path),
                settings.currency,
            )

            QMessageBox.information(
                self, "Export Excel", ("Excel exporté :\n\n" f"{output}")
            )

        except Exception as exc:

            QMessageBox.critical(self, "Erreur Export Excel", str(exc))

    def open_exports_folder(self):

        try:

            settings = self.settings_service.get()

            exports_dir = Path(settings.export_directory)

            exports_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            if os.name == "nt":

                os.startfile(exports_dir.resolve())

            else:

                subprocess.run(["xdg-open", str(exports_dir.resolve())], check=False)

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Erreur",
                ("Impossible d'ouvrir le " "dossier exports.\n\n" f"{exc}"),
            )

    def refresh(self):

        self.settings = self.settings_service.get()

        self.load_reports()
