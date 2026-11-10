# Orchestrateur des exports
from src.reports.excel_report import ExcelReport
from src.reports.pdf_report import PdfReport


class ReportGenerator:

    @staticmethod
    def generate(report_type, estimation, output_file):

        generators = {
            "pdf": PdfReport,
            "xlsx": ExcelReport,
        }

        generator = generators.get(report_type)

        if not generator:
            raise ValueError(f"Unsupported format: {report_type}")

        return generator.generate(estimation, output_file)
