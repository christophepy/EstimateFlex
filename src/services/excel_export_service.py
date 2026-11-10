"""
Export Excel des rapports EstimateFlex.
"""

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import (
    Alignment,
    Border,
    Font,
    PatternFill,
    Side,
)


class ExcelExportService:

    @staticmethod
    def export(report, file_path: str) -> Path:
        """
        Exporte un rapport d'estimation au format Excel.
        """

        wb = Workbook()

        ws = wb.active
        ws.title = "Résumé"

        # ==================================================
        # STYLES
        # ==================================================

        blue_fill = PatternFill(fill_type="solid", fgColor="1976D2")

        header_font = Font(bold=True, color="FFFFFF")

        bold_font = Font(bold=True)

        thin = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin"),
        )

        date_only = str(report.created_at)[:10]

        formatted_cost = f"{report.estimated_cost:,.2f}".replace(",", " ").replace(
            ".", ","
        )

        # ==================================================
        # TITRE
        # ==================================================

        ws.merge_cells("A1:B1")

        title = ws["A1"]

        title.value = "EstimateFlex - Rapport d'Estimation"

        title.font = Font(bold=True, size=14, color="FFFFFF")

        title.fill = blue_fill

        title.alignment = Alignment(horizontal="center", vertical="center")

        # ==================================================
        # EN-TÊTES
        # ==================================================

        headers = ["Champ", "Valeur"]

        for col, header in enumerate(headers, start=1):

            cell = ws.cell(row=3, column=col, value=header)

            cell.font = header_font
            cell.fill = blue_fill
            cell.border = thin

        # ==================================================
        # DONNÉES
        # ==================================================

        data = [
            ["Nom", str(report.estimation_nom)],
            ["Projet", str(report.project_nom)],
            ["Scénario", str(report.scenario_nom)],
            ["Charge (h)", f"{report.estimated_hours:.2f} h"],
            ["Durée (j)", f"{report.estimated_days:.2f} j"],
            ["Coût (€)", f"{formatted_cost} €"],
            ["Facteur de risque", f"{report.risk_factor:.2f}"],
            ["Date", date_only],
        ]

        for row_num, (key, value) in enumerate(data, start=4):

            c1 = ws.cell(row=row_num, column=1, value=key)

            c2 = ws.cell(row=row_num, column=2, value=value)

            c1.font = bold_font

            c1.border = thin
            c2.border = thin

        # ==================================================
        # MISE EN PAGE
        # ==================================================

        ws.column_dimensions["A"].width = 25
        ws.column_dimensions["B"].width = 35

        ws.freeze_panes = "A4"

        # ==================================================
        # SAUVEGARDE
        # ==================================================

        output = Path(file_path)

        if output.suffix.lower() != ".xlsx":
            output = output.with_suffix(".xlsx")

        output = ExcelExportService._get_versioned_filename(output)

        wb.save(output)

        return output

    @staticmethod
    def _get_versioned_filename(output: Path) -> Path:

        base = output.stem
        suffix = output.suffix

        version = 1

        while True:

            candidate = output.with_name(f"{base}_V{version:02d}{suffix}")

            if not candidate.exists():
                return candidate

            version += 1
