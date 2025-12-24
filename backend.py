import os
from io import BytesIO
from groq import Groq
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# -------------------------
# GROQ CLIENT
# -------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found")

client = Groq(api_key=GROQ_API_KEY)

# ======================================================
# SIGNAL-BASED HR DECISION AGENT
# ======================================================
def generate_hr_decision(context: dict) -> str:
    """
    Uses aggregated HR signals instead of raw data
    """

    prompt = f"""
You are an Enterprise HR Intelligence Analyst.

You are provided with:
• Aggregated HR signals (pre-computed)
• Company HR policies
• A business question

-----------------------------
HR SIGNALS
-----------------------------
{context["hr_signals"]}

-----------------------------
COMPANY POLICIES
-----------------------------
{context["company_policies"]}

-----------------------------
USER QUESTION
-----------------------------
{context["user_question"]}

-----------------------------
INSTRUCTIONS
-----------------------------
• Answer organization-wide HR questions
• Use signals to identify risks and patterns
• Mention employee IDs only from provided samples
• Keep output formal, structured, and audit-ready
• No emojis
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You analyze HR signals, not raw datasets."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.15
    )

    return response.choices[0].message.content


# ======================================================
# CLOUD-SAFE PDF GENERATOR
# ======================================================
def generate_pdf_report(report_text: str) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Compunnel – HR Intelligence Report</b>", styles["Title"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    for line in report_text.split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
