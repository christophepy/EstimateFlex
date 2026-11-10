# Export Excel
from openpyxl import Workbook


class ExcelReport:

    @staticmethod
    def generate(estimation, output_file):

        wb = Workbook()

        ws = wb.active

        ws.title = "Estimation"

        ws["A1"] = "Project"
        ws["B1"] = estimation.project_nom

        ws["A2"] = "Cost"
        ws["B2"] = estimation.total_cost

        ws["A3"] = "Duration"
        ws["B3"] = estimation.duration_days

        wb.save(output_file)

        return output_file
