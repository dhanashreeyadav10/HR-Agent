import os
from groq import Groq

# -------------------------
# Load GROQ API Key
# -------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY missing. Add it to Streamlit Secrets or environment variables."
    )

client = Groq(api_key=GROQ_API_KEY)

# -------------------------
# HR Knowledge-Based Agent
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

You must:
• Analyze employee data deeply
• Apply company policies first
• Use general HR knowledge only if policy is silent
• Clearly explain decisions
• Maintain professional HR tone

=============================
EMPLOYEE DATA
=============================
{context["employee_data"]}

=============================
COMPANY POLICIES
=============================
{context["company_policies"]}

=============================
USER QUESTION
=============================
{context["user_question"]}

=============================
RESPONSE FORMAT
=============================
• Data-driven analysis
• Policy references
• Clear conclusion
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
