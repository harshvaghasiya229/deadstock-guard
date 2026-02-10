from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


def generate_pdf_report(df, filename, title="DeadStock Guard – Inventory Report"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename, pagesize=A4)

    elements = []
    elements.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    table_data = [df.columns.tolist()] + df.values.tolist()
    table = Table(table_data, repeatRows=1)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    doc.build(elements)


# ✅ NEW – does not affect old PDF
def generate_warehouse_pdfs(result_df):
    if "Warehouse" not in result_df.columns:
        return []

    files = []
    for wh in result_df["Warehouse"].dropna().unique():
        wh_df = result_df[result_df["Warehouse"] == wh]
        filename = f"deadstock_report_{wh}.pdf"
        generate_pdf_report(
            wh_df,
            filename,
            title=f"DeadStock Guard – Warehouse Report ({wh})"
        )
        files.append(filename)

    return files
