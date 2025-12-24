# import os
# from groq import Groq

# # -------------------------
# # Load GROQ key (Cloud-safe)
# # -------------------------
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# if not GROQ_API_KEY:
#     raise RuntimeError(
#         "GROQ_API_KEY is missing. "
#         "Add it in Streamlit Cloud → Settings → Secrets."
#     )

# client = Groq(api_key=GROQ_API_KEY)

# # -------------------------
# # AI Explanation
# # -------------------------
# def generate_ai_explanation(employee: dict) -> str:
#     prompt = f"""
# You are an HR Intelligence Agent.

# Employee data:
# {employee}

# Provide a detailed, structured HR explanation.
# Use bullet points and professional tone.
# """

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=[
#             {"role": "system", "content": "You are an expert HR analyst."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.3
#     )

#     return response.choices[0].message.content










import os
from groq import Groq

# -------------------------
# Load GROQ key
# -------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY missing in environment")

client = Groq(api_key=GROQ_API_KEY)

# -------------------------
# HR Knowledge Agent
# -------------------------
def generate_ai_explanation(context: dict) -> str:
    """
    context = {
        employee_data: dict,
        company_policies: str,
        user_question: str
    }
    """

    prompt = f"""
You are a senior HR Intelligence Agent.

You have access to:
1. Employee data (single source of truth)
2. Company HR policies from Staffline portal
3. General HR best practices

-----------------------------------
EMPLOYEE DATA:
{context['employee_data']}

-----------------------------------
COMPANY POLICIES:
{context['company_policies']}

-----------------------------------
USER QUESTION:
{context['user_question']}

-----------------------------------
INSTRUCTIONS:
- First analyze employee data deeply
- Apply relevant company policies explicitly
- Use general HR knowledge where policies are silent
- Clearly mention which policy or data point you are using
- If something is missing, highlight it
- Respond in structured bullet points
- Maintain professional HR tone
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert enterprise HR analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content




