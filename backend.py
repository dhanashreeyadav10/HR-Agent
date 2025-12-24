# import os
# from groq import Groq

# # -------------------------
# # Load GROQ API Key
# # -------------------------
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise RuntimeError(
#         "GROQ_API_KEY missing. Add it to Streamlit Secrets or environment variables."
#     )

# client = Groq(api_key=GROQ_API_KEY)

# # -------------------------
# # HR Knowledge-Based Agent
# # -------------------------
# def generate_ai_explanation(context: dict) -> str:
#     """
#     context = {
#         employee_data: dict,
#         company_policies: str,
#         user_question: str
#     }
#     """

#     prompt = f"""
# You are a senior HR Intelligence Agent.

# You must:
# • Analyze employee data deeply
# • Apply company policies first
# • Use general HR knowledge only if policy is silent
# • Clearly explain decisions
# • Maintain professional HR tone

# =============================
# EMPLOYEE DATA
# =============================
# {context["employee_data"]}

# =============================
# COMPANY POLICIES
# =============================
# {context["company_policies"]}

# =============================
# USER QUESTION
# =============================
# {context["user_question"]}

# =============================
# RESPONSE FORMAT
# =============================
# • Data-driven analysis
# • Policy references
# • Clear conclusion
# """

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=[
#             {"role": "system", "content": "You are an expert enterprise HR analyst."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.2
#     )

#     return response.choices[0].message.content

import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY missing")

client = Groq(api_key=GROQ_API_KEY)

def generate_ai_explanation(context: dict) -> str:
    """
    context = {
        staffline_employee: dict,
        staffline_policies: str,
        keka_finance: dict,
        unlocku_performance: dict,
        user_question: str
    }
    """

    prompt = f"""
You are a senior enterprise HR Intelligence Agent.

You have access to MULTIPLE SYSTEMS:

1️⃣ Staffline Portal
- Employee master data
- Company HR policies (authoritative)

2️⃣ Keka Portal
- Employee finance & payroll data

3️⃣ UnlockU Portal
- Employee performance & learning data

---------------------------------
STAFFLINE – EMPLOYEE DATA
---------------------------------
{context["staffline_employee"]}

---------------------------------
STAFFLINE – COMPANY POLICIES
---------------------------------
{context["staffline_policies"]}

---------------------------------
KEKA – FINANCE DATA
---------------------------------
{context["keka_finance"]}

---------------------------------
UNLOCKU – PERFORMANCE DATA
---------------------------------
{context["unlocku_performance"]}

---------------------------------
USER QUESTION
---------------------------------
{context["user_question"]}

---------------------------------
INSTRUCTIONS
---------------------------------
• Treat Staffline policies as highest authority
• Correlate finance & performance where relevant
• Use general HR best practices only if policies are silent
• Clearly explain which system supports each conclusion
• Respond in structured bullet points
• Provide a final recommendation
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an enterprise HR decision analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
