from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data, file_path):
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("Troll Detection Report", styles["Title"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"Text: {data.get('text','')}", styles["Normal"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"Label: {data.get('label','')}", styles["Normal"]))
    elements.append(Paragraph(f"Confidence: {data.get('confidence',0)}", styles["Normal"]))

    legal = data.get("legal", {})
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Crime: {legal.get('crime','')}", styles["Normal"]))
    elements.append(Paragraph(f"Law: {legal.get('law','')}", styles["Normal"]))

    actions = legal.get("actions", [])
    for act in actions:
        elements.append(Paragraph(f"- {act}", styles["Normal"]))

    doc.build(elements)