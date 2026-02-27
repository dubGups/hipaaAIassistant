from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def build_hipaa_pdf(org_context: dict, summary: str, overall_level: str, findings: list[dict]) -> bytes:
    """
    Returns a PDF as bytes.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
        title="HIPAA Security Risk Assessment"
    )

    styles = getSampleStyleSheet()
    story = []

    # Header
    story.append(Paragraph("Complisstant HIPAA Security Risk Assessment", styles["Title"]))
    story.append(Spacer(1, 8))

    org_name = org_context.get("organization") or "N/A"
    org_type = org_context.get("type") or "N/A"
    employees = org_context.get("employees") or "N/A"
    uses_msp = org_context.get("uses_msp") or "N/A"
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")

    meta_table_data = [
        ["Organization", org_name],
        ["Organization Type", org_type],
        ["Employees", employees],
        ["Uses MSP", uses_msp],
        ["Generated", generated],
        ["Overall Risk Level", overall_level],
    ]

    meta_table = Table(meta_table_data, colWidths=[160, 360])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # Executive Summary
    story.append(Paragraph("Executive Summary", styles["Heading2"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(summary.replace("\n", "<br/>"), styles["BodyText"]))
    story.append(Spacer(1, 14))

    # Findings Overview Table
    story.append(Paragraph("Findings Overview", styles["Heading2"]))
    story.append(Spacer(1, 6))

    if findings:
        overview_data = [["Risk", "Finding Title", "HIPAA Citation", "Score"]]
        for f in findings:
            overview_data.append([
                f.get("risk_level", "N/A"),
                f.get("title", "N/A"),
                f.get("citation", "N/A"),
                str(f.get("score", "N/A")),
            ])

        overview_table = Table(overview_data, colWidths=[60, 280, 120, 60], repeatRows=1)
        overview_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(overview_table)
    else:
        story.append(Paragraph("No findings were triggered based on responses.", styles["BodyText"]))

    story.append(PageBreak())

    # Detailed Findings
    story.append(Paragraph("Detailed Findings", styles["Heading2"]))
    story.append(Spacer(1, 10))

    if findings:
        for idx, f in enumerate(findings, start=1):
            title = f.get("title", "N/A")
            citation = f.get("citation", "N/A")
            risk_level = f.get("risk_level", "N/A")
            likelihood = f.get("likelihood", "N/A")
            impact = f.get("impact", "N/A")
            score = f.get("score", "N/A")
            observation = f.get("observation", "N/A")
            recommendation = f.get("recommendation", "N/A")

            story.append(Paragraph(f"{idx}. {title}", styles["Heading3"]))
            story.append(Spacer(1, 6))

            detail_table_data = [
                ["HIPAA Citation", citation],
                ["Risk Level", risk_level],
                ["Likelihood", str(likelihood)],
                ["Impact", str(impact)],
                ["Score", str(score)],
            ]
            detail_table = Table(detail_table_data, colWidths=[120, 400])
            detail_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]))
            story.append(detail_table)
            story.append(Spacer(1, 10))

            story.append(Paragraph("<b>Observation</b>", styles["BodyText"]))
            story.append(Paragraph(observation.replace("\n", "<br/>"), styles["BodyText"]))
            story.append(Spacer(1, 8))

            story.append(Paragraph("<b>Recommendation</b>", styles["BodyText"]))
            story.append(Paragraph(recommendation.replace("\n", "<br/>"), styles["BodyText"]))
            story.append(Spacer(1, 14))
    else:
        story.append(Paragraph("No detailed findings to display.", styles["BodyText"]))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes