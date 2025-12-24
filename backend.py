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
# DYNAMIC HR DECISION AGENT (INDIVIDUAL + POPULATION)
# ======================================================
def generate_hr_decision(context: dict) -> str:
    """
    Handles both:
    - Individual employee decisions
    - Organization-wide HR analytics questions
    """

    prompt = f"""
You are a Senior Enterprise HR Intelligence System.

You have access to FULL ORGANIZATIONAL DATA from:
- Staffline (employee master + policies)
- Keka (finance & payroll)
- UnlockU (performance & learning)

DATASETS PROVIDED:
• Employee Master (multiple employees)
• Finance Data (multiple employees)
• Performance Data (multiple employees)
• Company Policies

----------------------------------
EMPLOYEE MASTER DATA
----------------------------------
{context["staffline_employee_data"]}

----------------------------------
FINANCE DATA
----------------------------------
{context["keka_finance_data"]}

----------------------------------
PERFORMANCE DATA
----------------------------------
{context["unlocku_performance_data"]}

----------------------------------
COMPANY POLICIES
----------------------------------
{context["staffline_policies"]}

----------------------------------
USER QUESTION
----------------------------------
{context["user_question"]}

----------------------------------
INSTRUCTIONS (CRITICAL)
----------------------------------
1. FIRST determine the question type:
   - Individual employee question
   - Organization-wide / population analysis question

2. If POPULATION analysis:
   - Identify relevant risk signals (performance, payroll, learning, tenure)
   - Return a LIST or SUMMARY of employees
   - Mention WHY they are flagged
   - Do NOT require employee_id selection

3. If INDIVIDUAL analysis:
   - Provide a formal HR Decision Report

4. OUTPUT FORMAT:
   - Clear headings
   - Bullet points
   - Formal HR tone
   - Audit-ready language
   - No emojis
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an enterprise HR analytics and decision engine."},
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
