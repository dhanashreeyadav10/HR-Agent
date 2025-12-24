# import os
# from groq import Groq

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise RuntimeError("GROQ_API_KEY missing")

# client = Groq(api_key=GROQ_API_KEY)

# def generate_ai_explanation(context: dict) -> str:
#     """
#     context = {
#         staffline_employee: dict,
#         staffline_policies: str,
#         keka_finance: dict,
#         unlocku_performance: dict,
#         user_question: str
#     }
#     """

#     prompt = f"""
# You are a senior enterprise HR Intelligence Agent.

# You have access to MULTIPLE SYSTEMS:

# 1️⃣ Staffline Portal
# - Employee master data
# - Company HR policies (authoritative)

# 2️⃣ Keka Portal
# - Employee finance & payroll data

# 3️⃣ UnlockU Portal
# - Employee performance & learning data

# ---------------------------------
# STAFFLINE – EMPLOYEE DATA
# ---------------------------------
# {context["staffline_employee"]}

# ---------------------------------
# STAFFLINE – COMPANY POLICIES
# ---------------------------------
# {context["staffline_policies"]}

# ---------------------------------
# KEKA – FINANCE DATA
# ---------------------------------
# {context["keka_finance"]}

# ---------------------------------
# UNLOCKU – PERFORMANCE DATA
# ---------------------------------
# {context["unlocku_performance"]}

# ---------------------------------
# USER QUESTION
# ---------------------------------
# {context["user_question"]}

# ---------------------------------
# INSTRUCTIONS
# ---------------------------------
# • Treat Staffline policies as highest authority
# • Correlate finance & performance where relevant
# • Use general HR best practices only if policies are silent
# • Clearly explain which system supports each conclusion
# • Respond in structured bullet points
# • Provide a final recommendation
# """

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=[
#             {"role": "system", "content": "You are an enterprise HR decision analyst."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.2
#     )

#     return response.choices[0].message.content


# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.pagesizes import A4

# # -------------------------
# # HR SUMMARY AGENT
# # -------------------------
# def generate_hr_summary(analysis_text: str) -> str:
#     """
#     Converts detailed HR analysis into an executive summary
#     """

#     prompt = f"""
# You are an HR Executive Summary Agent.

# Given the detailed HR analysis below:
# ----------------------------------
# {analysis_text}
# ----------------------------------

# Your task:
# • Summarize in simple, executive-friendly language
# • Highlight final decision
# • Mention key supporting reasons
# • Keep it concise (no more than 8 bullet points)
# """

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=[
#             {"role": "system", "content": "You summarize HR decisions for leadership."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.2
#     )

#     return response.choices[0].message.content


# # -------------------------
# # PDF REPORT GENERATOR
# # -------------------------
# def generate_pdf_report(employee_id: str, summary_text: str) -> str:
#     """
#     Creates a downloadable HR PDF report
#     """

#     file_path = f"/mnt/data/HR_Report_{employee_id}.pdf"

#     doc = SimpleDocTemplate(file_path, pagesize=A4)
#     styles = getSampleStyleSheet()
#     story = []

#     story.append(Paragraph("<b>HR Intelligence Report</b>", styles["Title"]))
#     story.append(Paragraph(f"<b>Employee ID:</b> {employee_id}", styles["Normal"]))
#     story.append(Paragraph("<br/>", styles["Normal"]))

#     for line in summary_text.split("\n"):
#         story.append(Paragraph(line, styles["Normal"]))

#     doc.build(story)

#     return file_path

import os
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

Summarize the following HR analysis into:
• Final decision
• Key supporting reasons
• Risks (if any)
• Next recommended action

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
# PDF GENERATOR
# ======================================================
def generate_pdf_report(employee_id: str, summary_text: str) -> str:

    file_path = f"/mnt/data/HR_Report_{employee_id}.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Compunnel – HR Intelligence Report</b>", styles["Title"]))
    story.append(Paragraph(f"<b>Employee ID:</b> {employee_id}", styles["Normal"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    for line in summary_text.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))

    doc.build(story)

    return file_path
