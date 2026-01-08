# import os
# from io import BytesIO
# from groq import Groq
# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.pagesizes import A4

# # -------------------------
# # GROQ CLIENT
# # -------------------------
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise RuntimeError("GROQ_API_KEY not found")

# client = Groq(api_key=GROQ_API_KEY)

# # ======================================================
# # SIGNAL-BASED HR INTELLIGENCE AGENT
# # ======================================================
# def generate_hr_decision(context: dict) -> str:
#     """
#     Uses aggregated HR signals (NOT raw data)
#     """

#     prompt = f"""
# You are an Enterprise HR Intelligence Analyst.

# You are provided with:
# • Aggregated HR signals (computed outside the LLM)
# • Company HR policies
# • A business question

# -----------------------------
# HR SIGNALS
# -----------------------------
# {context["hr_signals"]}

# -----------------------------
# COMPANY POLICIES
# -----------------------------
# {context["company_policies"]}

# -----------------------------
# USER QUESTION
# -----------------------------
# {context["user_question"]}

# -----------------------------
# INSTRUCTIONS
# -----------------------------
# • Answer organization-wide HR questions
# • Identify risks, trends, and affected employees
# • Refer only to employee IDs present in the signal sample
# • Keep output formal, structured, and audit-ready
# • Do NOT request raw datasets
# • No emojis
# """

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=[
#             {"role": "system", "content": "You analyze HR signals, not raw datasets."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.15
#     )

#     return response.choices[0].message.content


# # ======================================================
# # CLOUD-SAFE PDF GENERATOR (IN-MEMORY)
# # ======================================================
# def generate_pdf_report(report_text: str) -> bytes:
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4)
#     styles = getSampleStyleSheet()
#     story = []

#     story.append(
#         Paragraph("<b>Compunnel – HR Intelligence Report</b>", styles["Title"])
#     )
#     story.append(Paragraph("<br/>", styles["Normal"]))

#     for line in report_text.split("\n"):
#         if line.strip():
#             story.append(Paragraph(line, styles["Normal"]))

#     doc.build(story)
#     buffer.seek(0)

#     return buffer.getvalue()



import os
import streamlit as st
from io import BytesIO
from groq import Groq
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

import streamlit as st
import os

st.write("🔑 Secret exists:", "GROQ_API_KEY" in st.secrets)
st.write("🔑 Env exists:", bool(os.getenv("GROQ_API_KEY")))

key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
st.write("🔑 Key prefix:", key[:6] if key else "None")

# ======================================================
# HR INTELLIGENCE AGENT
# ======================================================
def generate_hr_decision(context: dict) -> str:

    prompt = f"""
You are an Enterprise HR Intelligence Analyst.

HR SIGNALS:
{context["hr_signals"]}

COMPANY POLICIES:
{context["company_policies"]}

USER QUESTION:
{context["user_question"]}

INSTRUCTIONS:
- Answer at organization level
- Identify risks, trends, and impacted employees
- Refer only to employee IDs provided
- Output must be audit-ready
- Do not request raw datasets
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You analyze HR signals only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.15
    )

    return response.choices[0].message.content

# ======================================================
# PDF REPORT GENERATOR
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

