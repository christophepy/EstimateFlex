"""
EstimateFlex - Main Window
Version 1.0 MVP
"""

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QTabWidget,
)

from src.persistence.estimation_repository import EstimationRepository

# Tabs
from src.ui.dashboard_tab import DashboardTab
from src.ui.estimation_tab import EstimationTab
from src.ui.profiles_tab import ProfilesTab
from src.ui.projects_tab import ProjectsTab
from src.ui.reports_tab import ReportsTab
from src.ui.scenarios_tab import ScenariosTab


class MainWindow(QMainWindow):
    """
    Fenêtre principale EstimateFlex
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("EstimateFlex v1.0")
        self.resize(1600, 900)

        self.estimation_repository = EstimationRepository()

        self._create_ui()
        self._create_menu()
        self._create_statusbar()

    # ==========================================================
    # UI
    # ==========================================================

    def _create_ui(self):
        """
        Construction interface
        """

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)

        self.tabs.currentChanged.connect(self.on_tab_changed)

        self.projects_tab = ProjectsTab()

        self.profiles_tab = ProfilesTab()

        self.estimation_tab = EstimationTab()

        self.scenarios_tab = ScenariosTab()

        self.reports_tab = ReportsTab(self.estimation_repository)

        self.dashboard_tab = DashboardTab(self.estimation_repository)

        self.tabs.addTab(self.projects_tab, "📁 Projects")

        self.tabs.addTab(self.profiles_tab, "👤 Profiles")

        self.tabs.addTab(self.estimation_tab, "⚙️ Estimation")

        self.tabs.addTab(self.scenarios_tab, "📈 Scenarios")

        self.tabs.addTab(self.reports_tab, "📄 Reports")

        self.tabs.addTab(self.dashboard_tab, "Dashboard")

        self.setCentralWidget(self.tabs)

    # ==========================================================
    # MENU
    # ==========================================================

    def _create_menu(self):
        """
        Barre de menu principale
        """

        menubar = self.menuBar()

        # ---------- FILE ----------

        file_menu = menubar.addMenu("&File")

        action_new = QAction("New Project", self)

        action_open = QAction("Open Project", self)

        action_save = QAction("Save Project", self)

        action_exit = QAction("Exit", self)

        action_exit.triggered.connect(self.close)

        file_menu.addAction(action_new)
        file_menu.addAction(action_open)
        file_menu.addAction(action_save)
        file_menu.addSeparator()
        file_menu.addAction(action_exit)

        # ---------- ESTIMATION ----------

        estimation_menu = menubar.addMenu("&Estimation")

        action_run = QAction("Run Estimation", self)

        action_run.triggered.connect(self.run_estimation)

        estimation_menu.addAction(action_run)

        # ---------- REPORTS ----------

        reports_menu = menubar.addMenu("&Reports")

        action_export_pdf = QAction("Export PDF", self)

        action_export_excel = QAction("Export Excel", self)

        reports_menu.addAction(action_export_pdf)

        reports_menu.addAction(action_export_excel)

        # ---------- HELP ----------

        help_menu = menubar.addMenu("&Help")

        action_about = QAction("About", self)

        action_about.triggered.connect(self.show_about)

        help_menu.addAction(action_about)

    # ==========================================================
    # STATUS BAR
    # ==========================================================

    def _create_statusbar(self):
        """
        Barre de statut
        """

        self.statusBar().showMessage("Ready")

    # ==========================================================
    # ACTIONS
    # ==========================================================

    def run_estimation(self):
        """
        Lance un calcul d'estimation
        """

        try:

            self.statusBar().showMessage("Running estimation...")

            if hasattr(self.estimation_tab, "run_estimation"):
                self.estimation_tab.run_estimation()

            self.statusBar().showMessage("Estimation completed")

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Estimation Error",
                str(exc),
            )

            self.statusBar().showMessage("Estimation failed")

    def show_about(self):
        """
        Fenêtre A propos
        """

        QMessageBox.about(
            self,
            "EstimateFlex",
            (
                "EstimateFlex v1.0\n\n"
                "Project Estimation Platform\n\n"
                "Features:\n"
                "- Cost Estimation\n"
                "- Duration Estimation\n"
                "- Workload Estimation\n"
                "- Scenarios Analysis\n"
                "- Excel Reports\n"
                "- PDF Reports"
            ),
        )

    def on_tab_changed(
        self,
        index,
    ):
        """
        Rafraîchissement automatique
        des onglets lors de leur activation.
        """

        widget = self.tabs.widget(index)

        if hasattr(widget, "refresh"):

            try:

                widget.refresh()

            except Exception as exc:

                print(f"Erreur refresh " f"{type(widget).__name__} : " f"{exc}")

    # ==========================================================
    # EVENTS
    # ==========================================================

    def closeEvent(self, event):  # pylint: disable=invalid-name
        """
        Confirmation fermeture
        """

        reply = QMessageBox.question(
            self,
            "Exit",
            "Do you really want to quit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
