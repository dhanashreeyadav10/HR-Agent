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
# HR FINAL DECISION AGENT (MERGED)
# ======================================================
def generate_final_hr_report(context: dict) -> str:
    """
    Generates a clean, formal, audit-ready HR Decision Report
    """

    prompt = f"""
You are a Senior HR Decision Authority preparing an official HR report.

Authoritative Systems:
- Staffline: Employee master & company policies (highest authority)
- Keka: Payroll & finance data
- UnlockU: Performance & learning data

Do NOT expose raw data.
Do NOT show internal reasoning.
Write a clean, formal HR report.

==============================
EMPLOYEE DATA (STAFFLINE)
==============================
{context["staffline_employee"]}

==============================
COMPANY POLICIES (STAFFLINE)
==============================
{context["staffline_policies"]}

==============================
FINANCE DATA (KEKA)
==============================
{context["keka_finance"]}

==============================
PERFORMANCE DATA (UNLOCKU)
==============================
{context["unlocku_performance"]}

==============================
USER QUERY
==============================
{context["user_question"]}

==============================
OUTPUT FORMAT (STRICT)
==============================

HR DECISION REPORT

1. Employee Overview
- Role, department, employment type, tenure

2. Policy Evaluation
- Applicable policies
- Eligibility checks

3. Performance Assessment
- Performance status
- Learning compliance

4. Payroll & Compliance Review
- Payroll readiness
- Financial risks

5. Risks & Exceptions
- Clearly state risks or confirm none

6. Final HR Decision
- APPROVED / NOT APPROVED / CONDITIONAL
- Short justification

7. Recommended Next Actions
- Clear, actionable HR steps

Tone:
- Formal
- Professional
- Audit-ready
- Bullet points only
- No emojis
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You write official enterprise HR decision reports."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.15
    )

    return response.choices[0].message.content


# ======================================================
# CLOUD-SAFE PDF GENERATOR (IN-MEMORY)
# ======================================================
def generate_pdf_report(report_text: str) -> bytes:
    """
    Generates HR report PDF in memory (Streamlit Cloud safe)
    """

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(
        Paragraph("<b>Compunnel – HR Decision Report</b>", styles["Title"])
    )
    story.append(Paragraph("<br/>", styles["Normal"]))

    for line in report_text.split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["Normal"]))

    doc.build(story)
    buffer.seek(0)

    return buffer.getvalue()
