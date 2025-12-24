# import streamlit as st
# import pandas as pd
# import pdfplumber
# from PIL import Image
# import pytesseract
# from backend import generate_ai_explanation

# # -------------------------
# # PAGE CONFIG
# # -------------------------
# st.set_page_config(
#     page_title="HR Knowledge-Based Intelligence Agent",
#     layout="wide"
# )

# st.title("🧑‍💼 HR Knowledge-Based Intelligence Agent")
# st.caption("Employee data + Company policies → Policy-aware HR insights")

# # =========================
# # LEFT PANEL — BRANDING
# # =========================
# st.sidebar.image(
#     "compunnel_logo.jpg",
#     use_container_width=True
# )

# st.sidebar.header("📥 Knowledge Base Upload")

# # =========================
# # UPLOAD FILES
# # =========================
# emp_file = st.sidebar.file_uploader(
#     "Upload Employee Data (CSV / Excel)",
#     type=["csv", "xlsx"]
# )

# policy_file = st.sidebar.file_uploader(
#     "Upload Company Policy (PDF / TXT / Image)",
#     type=["pdf", "txt", "png", "jpg", "jpeg"]
# )

# employee_df = None
# employee_data = None
# company_policies = ""

# # -------------------------
# # LOAD EMPLOYEE DATA
# # -------------------------
# if emp_file:
#     employee_df = (
#         pd.read_csv(emp_file)
#         if emp_file.name.endswith(".csv")
#         else pd.read_excel(emp_file)
#     )
#     st.sidebar.success("Employee data loaded")

# # -------------------------
# # LOAD POLICY DATA
# # -------------------------
# if policy_file:
#     try:
#         name = policy_file.name.lower()

#         if name.endswith(".txt"):
#             company_policies = policy_file.read().decode("utf-8")

#         elif name.endswith(".pdf"):
#             with pdfplumber.open(policy_file) as pdf:
#                 company_policies = "\n".join(
#                     page.extract_text() or "" for page in pdf.pages
#                 )

#         elif name.endswith((".png", ".jpg", ".jpeg")):
#             image = Image.open(policy_file)
#             company_policies = pytesseract.image_to_string(image)

#         st.sidebar.success("Company policy loaded")

#     except Exception as e:
#         st.sidebar.error(f"Policy extraction failed: {e}")

# # =========================
# # EMPLOYEE SELECTION
# # =========================
# if employee_df is not None:
#     st.sidebar.subheader("👤 Select Employee")

#     emp_id = st.sidebar.selectbox(
#         "Employee ID",
#         employee_df["employee_id"].astype(str)
#     )

#     employee_data = (
#         employee_df[employee_df["employee_id"].astype(str) == emp_id]
#         .iloc[0]
#         .to_dict()
#     )

#     # Minimal info only (no JSON on main screen)
#     st.sidebar.markdown(
#         f"""
#         **Name:** {employee_data.get('name', 'N/A')}  
#         **Department:** {employee_data.get('department', 'N/A')}  
#         **Status:** {employee_data.get('employment_status', 'N/A')}
#         """
#     )

# # =========================
# # RIGHT PANEL — QUERY & OUTPUT
# # =========================
# if employee_data:

#     st.subheader("🧠 HR Intelligence Query")

#     user_query = st.text_area(
#         "Ask a policy-aware HR question",
#         height=120,
#         placeholder="Is this employee eligible for WFH as per company policy?"
#     )

#     if st.button("🔍 Get HR Insight", use_container_width=True):

#         if not company_policies.strip():
#             st.error("❌ Please upload company policy")
#         elif not user_query.strip():
#             st.error("❌ Please enter a question")
#         else:
#             with st.spinner("Analyzing employee data & policies..."):
#                 context = {
#                     "employee_data": employee_data,      # hidden
#                     "company_policies": company_policies,
#                     "user_question": user_query
#                 }

#                 response = generate_ai_explanation(context)

#             st.markdown("### 📊 AI Output")
#             st.markdown(response)

# else:
#     st.info("⬅ Upload employee data and company policy to begin")


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
