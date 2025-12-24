import os
from groq import Groq

# -------------------------
# Load API Key
# -------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Set it in environment variables.")

client = Groq(api_key=GROQ_API_KEY)

# -------------------------
# AI Explanation Generator
# -------------------------
def generate_ai_explanation(employee: dict) -> str:
    """
    Generates a detailed HR-grade explanation using LLM.
    """

    prompt = f"""
You are an HR Intelligence Agent.

Here is the employee data:
{employee}

Explain this employee's current HR status in a clear, structured, and professional way.
Use bullet points and headings.
Avoid generic statements.
Be factual and HR-grade.
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
