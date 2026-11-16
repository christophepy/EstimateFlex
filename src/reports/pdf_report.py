# Export PDF
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from src.utils.formatters import format_number


class PdfReport:

    @staticmethod
    def generate(estimation, output_file):

        doc = SimpleDocTemplate(output_file)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(Paragraph("EstimateFlex Report", styles["Title"]))

        elements.append(Spacer(1, 12))

        elements.append(
            Paragraph(
                ("Coût : " f"{format_number(estimation.total_cost)}"),
                styles["BodyText"],
            )
        )

        elements.append(
            Paragraph(f"Cost : {estimation.total_cost:.2f}", styles["BodyText"])
        )

        doc.build(elements)

        return output_file
