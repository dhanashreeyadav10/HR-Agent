# import streamlit as st
# from backend import generate_ai_explanation

# st.set_page_config(page_title="HR Agent", layout="wide")
# st.title("🧑‍💼 HR Employee Intelligence Agent")

# employee_data = {
#     "employee_id": 1002,
#     "name": "Anita Sharma",
#     "employment_type": "Full Time",
#     "pan": "ABCDE1234F",
#     "bank_account": "SBIN0001234",
#     "probation_end_date": "2023-07-10",
#     "manager_feedback": "Excellent performance and learning attitude",
#     "compliance_status": "READY",
#     "missing_items": [],
#     "lifecycle_state": "ACTIVE",
#     "confirmation_decision": "CONFIRM"
# }

# st.subheader("📄 Employee Record")
# st.json(employee_data)

# if st.button("🧠 Generate AI Explanation"):
#     with st.spinner("Analyzing employee data..."):
#         explanation = generate_ai_explanation(employee_data)

#     st.markdown("## 🧠 AI Explanation")
#     st.markdown(explanation)


import streamlit as st
import pandas as pd
import pdfplumber
from PIL import Image
import pytesseract
from backend import generate_ai_explanation

# 🔴 FORCE RESET (remove later if needed)
st.session_state.clear()

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="HR Knowledge-Based Intelligence Agent",
    layout="wide"
)

st.title("🧑‍💼 HR Knowledge-Based Intelligence Agent")
st.caption("Employee data + Company policies (PDF / TXT / Image) → HR Insights")

# =========================
# LEFT PANEL — UPLOADS
# =========================
st.sidebar.header("📥 Knowledge Base Upload")

# Employee Data
emp_file = st.sidebar.file_uploader(
    "Upload Employee Data (CSV / Excel)",
    type=["csv", "xlsx"]
)

# Policy Files
policy_file = st.sidebar.file_uploader(
    "Upload Company Policy (PDF / TXT / Image)",
    type=["pdf", "txt", "png", "jpg", "jpeg"]
)

employee_df = None
employee_data = None
company_policies = ""

# -------------------------
# LOAD EMPLOYEE DATA
# -------------------------
if emp_file:
    employee_df = (
        pd.read_csv(emp_file)
        if emp_file.name.endswith(".csv")
        else pd.read_excel(emp_file)
    )
    st.sidebar.success("Employee data loaded")

# -------------------------
# LOAD POLICY DATA
# -------------------------
if policy_file:
    file_name = policy_file.name.lower()

    try:
        if file_name.endswith(".txt"):
            company_policies = policy_file.read().decode("utf-8")

        elif file_name.endswith(".pdf"):
            with pdfplumber.open(policy_file) as pdf:
                pages = [page.extract_text() for page in pdf.pages]
            company_policies = "\n".join([p for p in pages if p])

        elif file_name.endswith((".png", ".jpg", ".jpeg")):
            image = Image.open(policy_file)
            company_policies = pytesseract.image_to_string(image)

        st.sidebar.success("Company policy loaded successfully")

    except Exception as e:
        st.sidebar.error(f"Policy extraction failed: {e}")

# =========================
# EMPLOYEE SELECTION
# =========================
if employee_df is not None:
    st.sidebar.subheader("👤 Select Employee")
    emp_id = st.sidebar.selectbox(
        "Employee ID",
        employee_df["employee_id"].astype(str)
    )

    employee_data = (
        employee_df[employee_df["employee_id"].astype(str) == emp_id]
        .iloc[0]
        .to_dict()
    )

# =========================
# RIGHT PANEL — ANALYSIS
# =========================
if employee_data:

    left, right = st.columns([1.3, 1.7])

    with left:
        st.subheader("📄 Employee Details")
        st.json(employee_data)

    with right:
        st.subheader("🧠 HR Intelligence Query")

        user_query = st.text_area(
            "Ask a policy-aware HR question",
            height=120,
            placeholder="Is this employee eligible for confirmation as per company policy?"
        )

        if st.button("🔍 Get HR Insight", use_container_width=True):

            if not company_policies.strip():
                st.error("❌ Please upload company policy")
            elif not user_query.strip():
                st.error("❌ Please enter a question")
            else:
                with st.spinner("Analyzing employee data & policies..."):
                    context = {
                        "employee_data": employee_data,
                        "company_policies": company_policies,
                        "user_question": user_query
                    }

                    response = generate_ai_explanation(context)

                st.markdown("### 📊 AI Output")
                st.markdown(response)

else:
    st.info("⬅ Upload employee data and company policy to begin")


