import os
from groq import Groq

# -------------------------
# Load GROQ key (Cloud-safe)
# -------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing. "
        "Add it in Streamlit Cloud → Settings → Secrets."
    )

client = Groq(api_key=GROQ_API_KEY)

# -------------------------
# AI Explanation
# -------------------------
def generate_ai_explanation(employee: dict) -> str:
    prompt = f"""
You are an HR Intelligence Agent.

Employee data:
{employee}

Provide a detailed, structured HR explanation.
Use bullet points and professional tone.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert HR analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
