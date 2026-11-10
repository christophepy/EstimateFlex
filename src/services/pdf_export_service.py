"""
Export PDF des rapports EstimateFlex
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class PdfExportService:

    @staticmethod
    def export(report, file_path: str) -> Path:

        output = Path(file_path)

        if output.suffix.lower() != ".pdf":
            output = output.with_suffix(".pdf")

        output = PdfExportService._get_versioned_filename(output)

        doc = SimpleDocTemplate(str(output))

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "EstimateFlexTitle",
            parent=styles["Title"],
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1976D2"),
        )

        elements = []

        # ==================================================
        # EN-TETE
        # ==================================================

        logo_path = (
            Path(__file__).resolve().parents[2]
            / "resources"
            / "images"
            / "estimateflex.png"
        )

        header_data = []

        if logo_path.exists():

            logo = Image(
                str(logo_path),
                width=35,
                height=35,
            )

            logo.hAlign = "LEFT"

            title_block = Paragraph(
                """
                <font size="18" color="#1976D2">
                <b>EstimateFlex</b>
                </font><br/>
                <font size="11">
                <b>Rapport d'Estimation</b>
                </font>
                """,
                styles["Normal"],
            )

            header_data.append([logo, title_block])

            header_table = Table(
                header_data,
                colWidths=[45, 250],
            )

            header_table.setStyle(
                TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ]
                )
            )

            elements.append(header_table)

        else:

            elements.append(
                Paragraph(
                    "EstimateFlex",
                    title_style,
                )
            )

        elements.append(Spacer(1, 80))

        # ==================================================
        # INFOS PROJET
        # ==================================================

        date_only = str(report.created_at)[:10]

        info_rows = [
            ["Projet", report.project_nom],
            ["Scénario", report.scenario_nom],
            ["Date", date_only],
        ]

        info_table = Table(info_rows, colWidths=[90, 180])

        info_table.hAlign = "LEFT"

        info_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.HexColor("#EAF2FB"),
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (0, -1),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                ]
            )
        )

        elements.append(info_table)

        elements.append(Spacer(1, 40))

        # ==================================================
        # DONNEES ESTIMATION
        # ==================================================

        formatted_cost = f"{report.estimated_cost:,.2f}".replace(",", " ").replace(
            ".", ","
        )

        rows = [
            ["Champ", "Valeur"],
            ["Nom", str(report.estimation_nom)],
            ["Projet", str(report.project_nom)],
            ["Scénario", str(report.scenario_nom)],
            ["Charge (heures)", f"{report.estimated_hours:.2f} h"],
            ["Durée (jours)", f"{report.estimated_days:.2f} j"],
            ["Coût (€)", f"{formatted_cost} €"],
            ["Facteur de risque", f"{report.risk_factor:.2f}"],
            ["Date de génération", date_only],
        ]

        table = Table(rows, colWidths=[130, 190])

        table.hAlign = "LEFT"

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#1976D2"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.black,
                    ),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (0, -1),
                        colors.HexColor("#EAF2FB"),
                    ),
                ]
            )
        )

        elements.append(table)

        # ==================================================
        # PIED DE PAGE
        # ==================================================

        def footer(canvas, doc):
            canvas.saveState()

            canvas.setFont("Helvetica-Oblique", 9)

            canvas.setFillColor(colors.grey)

            canvas.drawString(
                doc.leftMargin,
                15,
                "Document généré automatiquement par EstimateFlex v1.0",
            )

            canvas.restoreState()

        doc.build(
            elements,
            onFirstPage=footer,
            onLaterPages=footer,
        )

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
