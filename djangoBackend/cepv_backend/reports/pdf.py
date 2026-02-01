from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


def generate_dataset_pdf(dataset):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 40

    p.setFont("Helvetica-Bold", 26)
    p.drawString(40, y, "Chemical Equipment Dataset Report")

    
    summary = dataset.summary

    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "Summary Statistics")

    y -= 25
    p.setFont("Helvetica", 10)
    p.drawString(40, y, f"Total Equipment: {summary['total_equipment']}")
    y -= 15
    p.drawString(40, y, f"Average Flowrate: {summary['average_flowrate']:.2f}")
    y -= 15
    p.drawString(40, y, f"Average Pressure: {summary['average_pressure']:.2f}")
    y -= 15
    p.drawString(40, y, f"Average Temperature: {summary['average_temperature']:.2f}")

    y -= 30
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "Equipment Type Distribution")

    y -= 25
    p.setFont("Helvetica", 10)
    for eq_type, count in summary["type_distribution"].items():
        p.drawString(40, y, f"{eq_type}: {count}")
        y -= 15

    y -= 40
    p.setFont("Helvetica", 10)
    p.drawString(40, y, f"Filename: {dataset.filename}")
    y -= 20
    p.drawString(40, y, f"Uploaded At: {dataset.uploaded_at}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
