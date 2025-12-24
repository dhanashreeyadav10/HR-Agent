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
# AGENT 1 — HR INTELLIGENCE (DETAILED ANALYSIS)
# ======================================================
def generate_ai_explanation(context: dict) -> str:
    prompt = f"""
You are a Senior Enterprise HR Intelligence Agent.

SYSTEMS:
- Staffline: Employee master & company policies (highest authority)
- Keka: Finance & payroll
- UnlockU: Performance & learning

--------------------------------
STAFFLINE — EMPLOYEE DATA
--------------------------------
{context["staffline_employee"]}

--------------------------------
STAFFLINE — COMPANY POLICIES
--------------------------------
{context["staffline_policies"]}

--------------------------------
KEKA — FINANCE DATA
--------------------------------
{context["keka_finance"]}

--------------------------------
UNLOCKU — PERFORMANCE DATA
--------------------------------
{context["unlocku_performance"]}

--------------------------------
USER QUESTION
--------------------------------
{context["user_question"]}

--------------------------------
INSTRUCTIONS
--------------------------------
• Apply company policies first
• Correlate finance and performance
• Highlight risks or blockers
• Use bullet points
• Provide clear HR recommendation
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert HR analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# ======================================================
# AGENT 2 — HR SUMMARY AGENT
# ======================================================
def generate_hr_summary(analysis_text: str) -> str:
    prompt = f"""
You are an HR Executive Summary Agent.

Summarize the analysis into:
• Final decision
• Key supporting reasons
• Risks (if any)
• Recommended next action

Limit to 6–8 bullet points.

--------------------------------
{analysis_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You summarize HR decisions for leadership."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# ======================================================
# CLOUD-SAFE PDF GENERATOR (IN-MEMORY)
# ======================================================
def generate_pdf_report(summary_text: str) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Compunnel – HR Intelligence Report</b>", styles["Title"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    for line in summary_text.split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["Normal"]))

    doc.build(story)
    buffer.seek(0)

    return buffer.getvalue()
