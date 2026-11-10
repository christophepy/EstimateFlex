# ui/dashboard_tab.py
from collections import Counter
from statistics import mean

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
)
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class DashboardTab(QWidget):

    def __init__(
        self,
        estimation_repository,
        parent=None,
    ):
        super().__init__(parent)

        self.estimation_repository = estimation_repository

        self._build_ui()
        self.load_data()

    # ==========================================================
    # UI
    # ==========================================================

    def _build_ui(self):

        layout = QVBoxLayout(self)

        layout.setSpacing(12)

        layout.setContentsMargins(10, 10, 10, 10)

        # ------------------------------------------------------
        # KPI
        # ------------------------------------------------------

        kpi_group = QGroupBox("Indicateurs clés")
        kpi_group.setMaximumHeight(100)

        kpi_layout = QGridLayout()

        kpi_layout.setVerticalSpacing(2)
        kpi_layout.setHorizontalSpacing(30)

        self.lbl_count = QLabel("0")
        self.lbl_hours = QLabel("0 h")
        self.lbl_days = QLabel("0 j")
        self.lbl_cost = QLabel("0 €")

        self.lbl_total_cost = QLabel("0 €")
        self.lbl_max_cost = QLabel("0 €")
        self.lbl_min_cost = QLabel("0 €")
        self.lbl_best_profile = QLabel("-")

        for lbl in (
            self.lbl_count,
            self.lbl_hours,
            self.lbl_days,
            self.lbl_cost,
            self.lbl_total_cost,
            self.lbl_max_cost,
            self.lbl_min_cost,
            self.lbl_best_profile,
        ):

            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl.setStyleSheet("""
                font-size:26px;
                font-weight:bold;
                color:#1976D2;
                """)

        kpi_layout.addWidget(QLabel("Estimations"), 0, 0)
        kpi_layout.addWidget(QLabel("Charge moyenne"), 0, 1)
        kpi_layout.addWidget(QLabel("Durée moyenne"), 0, 2)
        kpi_layout.addWidget(QLabel("Coût moyen"), 0, 3)
        kpi_layout.addWidget(QLabel("Budget total"), 0, 4)
        kpi_layout.addWidget(QLabel("Coût max"), 0, 5)
        kpi_layout.addWidget(QLabel("Coût min"), 0, 6)
        kpi_layout.addWidget(QLabel("Profil principal"), 0, 7)

        kpi_layout.addWidget(self.lbl_count, 1, 0)
        kpi_layout.addWidget(self.lbl_hours, 1, 1)
        kpi_layout.addWidget(self.lbl_days, 1, 2)
        kpi_layout.addWidget(self.lbl_cost, 1, 3)
        kpi_layout.addWidget(self.lbl_total_cost, 1, 4)
        kpi_layout.addWidget(self.lbl_max_cost, 1, 5)
        kpi_layout.addWidget(self.lbl_min_cost, 1, 6)
        kpi_layout.addWidget(self.lbl_best_profile, 1, 7)

        for col in range(8):
            kpi_layout.setColumnStretch(col, 1)

        kpi_layout.setHorizontalSpacing(25)
        kpi_layout.setVerticalSpacing(5)

        kpi_group.setLayout(kpi_layout)

        layout.addWidget(kpi_group)

        self.lbl_last_estimation = QLabel("Dernière estimation : -")

        self.lbl_last_estimation.setStyleSheet("""
            font-size:14px;
            font-weight:bold;
            color:#555555;
            padding-left:10px;
            """)

        last_layout = QHBoxLayout()

        last_layout.addWidget(self.lbl_last_estimation)

        last_layout.addStretch()

        layout.addLayout(last_layout)

        # ------------------------------------------------------
        # Graphique
        # ------------------------------------------------------

        chart_group = QGroupBox("Estimations par scénario")

        chart_layout = QVBoxLayout()

        self.figure = Figure(figsize=(5, 2))

        self.canvas = FigureCanvasQTAgg(self.figure)

        self.cost_figure = Figure(figsize=(4, 2))

        self.cost_canvas = FigureCanvasQTAgg(self.cost_figure)

        chart_layout.addWidget(self.canvas)

        chart_group.setLayout(chart_layout)

        # ------------------------------------------------------
        # TOP 5
        # ------------------------------------------------------

        top_group = QGroupBox("Top 5 estimations les plus coûteuses")

        top_layout = QVBoxLayout()

        self.top_table = QTableWidget()

        self.top_table.setMaximumHeight(180)

        self.top_table.verticalHeader().setVisible(False)

        self.top_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.top_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.top_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.top_table.setAlternatingRowColors(True)

        self.top_table.setStyleSheet("""
            QTableView {
                alternate-background-color: #F5F9FF;
            }
            """)

        self.top_table.setColumnCount(5)

        self.top_table.setHorizontalHeaderLabels(
            [
                "Projet",
                "Profil",
                "Scénario",
                "Coût",
                "Date",
            ]
        )

        self.top_table.horizontalHeader().setStretchLastSection(True)

        top_layout.addWidget(self.top_table)

        top_group.setLayout(top_layout)

        middle_layout = QHBoxLayout()

        middle_layout.addWidget(chart_group, 3)

        middle_layout.addWidget(top_group, 2)

        layout.addLayout(middle_layout)

        # ------------------------------------------------------
        # Historique
        # ------------------------------------------------------

        history_group = QGroupBox("Dernières estimations")

        history_layout = QVBoxLayout()

        self.table = QTableWidget()

        self.table.setMaximumHeight(170)

        self.table.verticalHeader().setVisible(False)

        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableView {
                alternate-background-color: #F5F9FF;
            }
            """)

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels(
            [
                "Projet",
                "Profil",
                "Scénario",
                "Heures",
                "Coût",
                "Date",
            ]
        )

        self.table.horizontalHeader().setStretchLastSection(True)

        history_layout.addWidget(self.table)

        history_group.setLayout(history_layout)

        cost_group = QGroupBox("Répartition des coûts")

        cost_layout = QVBoxLayout()

        cost_layout.addWidget(self.cost_canvas)

        cost_group.setLayout(cost_layout)

        bottom_layout = QHBoxLayout()

        bottom_layout.addWidget(history_group, 3)

        bottom_layout.addWidget(cost_group, 2)

        layout.addLayout(bottom_layout)

        # ------------------------------------------------------
        # Bouton
        # ------------------------------------------------------

        buttons = QHBoxLayout()

        refresh_btn = QPushButton("Actualiser")

        refresh_btn.clicked.connect(self.load_data)

        buttons.addStretch()
        buttons.addWidget(refresh_btn)

        layout.addLayout(buttons)

    # ==========================================================
    # DATA
    # ==========================================================

    def load_data(self):

        reports = (
            self.estimation_repository.get_all() if self.estimation_repository else []
        )

        if not reports:

            self.lbl_count.setText("0")
            self.lbl_hours.setText("0 h")
            self.lbl_days.setText("0 j")
            self.lbl_cost.setText("0 €")

            self.lbl_last_estimation.setText("Dernière estimation : -")

            self.table.setRowCount(0)

            self._update_chart([])
            self._update_cost_chart([])

            return

        avg_hours = mean(r.estimated_hours for r in reports)

        avg_days = mean(r.estimated_days for r in reports)

        avg_cost = mean(r.estimated_cost for r in reports)

        total_cost = sum(r.estimated_cost for r in reports)

        max_cost = max(r.estimated_cost for r in reports)

        min_cost = min(r.estimated_cost for r in reports)

        profiles = {}

        for report in reports:

            profiles.setdefault(report.profile_nom, 0)

            profiles[report.profile_nom] += report.estimated_cost

        best_profile = max(profiles.items(), key=lambda item: item[1])[0]

        self.lbl_count.setText(str(len(reports)))

        self.lbl_hours.setText(f"{avg_hours:.2f} h")

        self.lbl_days.setText(f"{avg_days:.2f} j")

        self.lbl_cost.setText(f"{avg_cost:,.0f}".replace(",", " ") + " €")

        self.lbl_total_cost.setText(
            f"{total_cost:,.0f}".replace(",", " ").replace(".", ",") + " €"
        )

        self.lbl_max_cost.setText(
            f"{max_cost:,.0f}".replace(",", " ").replace(".", ",") + " €"
        )

        self.lbl_min_cost.setText(
            f"{min_cost:,.0f}".replace(",", " ").replace(".", ",") + " €"
        )

        self.lbl_best_profile.setText(best_profile)

        latest_report = max(reports, key=lambda r: str(r.created_at))

        latest_cost = f"{latest_report.estimated_cost:,.0f}".replace(",", " ")

        self.lbl_last_estimation.setText(
            "Dernière estimation : "
            f"{latest_report.project_nom} / "
            f"{latest_report.scenario_nom} / "
            f"{latest_cost} €"
        )

        self._update_chart(reports)

        self._update_cost_chart(reports)

        top_reports = sorted(
            reports,
            key=lambda r: r.estimated_cost,
            reverse=True,
        )[:5]

        self.top_table.setRowCount(len(top_reports))

        for row, report in enumerate(top_reports):

            cost = f"{report.estimated_cost:,.0f}".replace(",", " ").replace(".", ",")

            self.top_table.setItem(row, 0, QTableWidgetItem(str(report.project_nom)))

            self.top_table.setItem(row, 1, QTableWidgetItem(str(report.profile_nom)))

            self.top_table.setItem(row, 2, QTableWidgetItem(str(report.scenario_nom)))

            self.top_table.setItem(row, 3, QTableWidgetItem(f"{cost} €"))

            self.top_table.setItem(
                row, 4, QTableWidgetItem(str(report.created_at)[:10])
            )

        self.top_table.resizeColumnsToContents()

        reports = sorted(reports, key=lambda r: str(r.created_at), reverse=True)[:10]

        self.table.setRowCount(len(reports))

        for row, report in enumerate(reports):

            cost = f"{report.estimated_cost:,.2f}".replace(",", " ")

            self.table.setItem(row, 0, QTableWidgetItem(str(report.project_nom)))

            self.table.setItem(row, 1, QTableWidgetItem(str(report.profile_nom)))

            self.table.setItem(row, 2, QTableWidgetItem(str(report.scenario_nom)))

            self.table.setItem(
                row, 3, QTableWidgetItem(f"{report.estimated_hours:.2f}")
            )

            self.table.setItem(row, 4, QTableWidgetItem(f"{cost} €"))

            self.table.setItem(row, 5, QTableWidgetItem(str(report.created_at)[:10]))

        self.table.resizeColumnsToContents()

    # ==========================================================
    # GRAPHIQUE
    # ==========================================================

    def _update_chart(
        self,
        reports,
    ):

        self.figure.clear()

        ax = self.figure.add_subplot(111)

        if not reports:

            ax.set_title("Aucune donnée")

            self.canvas.draw()

            return

        scenarios = Counter(str(r.scenario_nom) for r in reports)

        ordre = [
            "Optimiste",
            "Réaliste",
            "Pessimiste",
        ]

        labels = []
        values = []

        for scenario in ordre:

            if scenario in scenarios:
                labels.append(scenario)
                values.append(scenarios[scenario])

        for scenario, value in scenarios.items():

            if scenario not in ordre:
                labels.append(scenario)
                values.append(value)

        bars = ax.bar(labels, values, color="#1976D2")

        for chart_bar in bars:

            height = chart_bar.get_height()

            ax.text(
                chart_bar.get_x() + chart_bar.get_width() / 2,
                height + 0.05,
                str(int(height)),
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                color="#333333",
            )

        ax.grid(axis="x", linestyle="--", alpha=0.3)

        ax.set_ylim(0, max(values) + 1)

        ax.set_title("Nombre d'estimations par scénario")

        ax.set_ylabel("Estimations")

        self.canvas.draw()

    def _update_cost_chart(
        self,
        reports,
    ):

        self.cost_figure.clear()

        ax = self.cost_figure.add_subplot(111)

        if not reports:

            ax.set_title("Aucune donnée")

            self.cost_canvas.draw()

            return

        top_costs = sorted(reports, key=lambda r: r.estimated_cost, reverse=True)[:5]

        labels = [f"{r.project_nom} [{r.scenario_nom}]" for r in top_costs]

        values = [r.estimated_cost for r in top_costs]

        ax.barh(labels, values, color="#42A5F5")

        ax.set_xlim(0, max(values) * 1.25)

        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1000:.0f} k€"))

        ax.grid(axis="x", linestyle="--", alpha=0.3)

        ax.set_title("Top coûts projets")

        # ax.set_xlabel(
        #    "Budget (k€)"
        # )

        ax.set_xlabel("")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        self.cost_figure.tight_layout()

        self.cost_canvas.draw()

    # ==========================================================
    # REFRESH
    # ==========================================================

    def refresh(self):
        self.load_data()
