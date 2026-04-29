from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data, file_path):
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Troll Detection Report", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Text:</b> {data.get('text','')}", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Prediction:</b> {data.get('label','')}", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Confidence:</b> {data.get('confidence','')}", styles["Normal"]))
    content.append(Spacer(1, 10))

    # ✅ Legal Section
    legal = data.get("legal", {})
    content.append(Paragraph(f"<b>Crime:</b> {legal.get('crime','')}", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Law:</b> {legal.get('law','')}", styles["Normal"]))
    content.append(Spacer(1, 10))

    for act in legal.get("actions", []):
        content.append(Paragraph(f"• {act}", styles["Normal"]))

    doc.build(content)