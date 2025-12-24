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
from backend import generate_ai_explanation

# 🔴 FORCE RESET (remove later)
st.session_state.clear()

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="HR Knowledge-Based Intelligence Agent",
    layout="wide"
)

st.markdown("## 🧑‍💼 HR Knowledge-Based Intelligence Agent")
st.markdown(
    "This system analyzes **employee data + company policies** "
    "and provides **policy-aware HR insights**."
)

# =========================
# LEFT PANEL — DATA UPLOAD
# =========================
st.sidebar.markdown("## 📥 Knowledge Base Upload")

emp_file = st.sidebar.file_uploader(
    "Upload Employee Master Data",
    type=["csv", "xlsx"]
)

policy_file = st.sidebar.file_uploader(
    "Upload Company Policies (Staffline)",
    type=["csv", "xlsx", "txt"]
)

employee_df = None
company_policies = ""

if emp_file:
    employee_df = (
        pd.read_csv(emp_file)
        if emp_file.name.endswith(".csv")
        else pd.read_excel(emp_file)
    )
    st.sidebar.success("Employee data loaded")

if policy_file:
    if policy_file.name.endswith(".txt"):
        company_policies = policy_file.read().decode("utf-8")
    else:
        df_policy = (
            pd.read_csv(policy_file)
            if policy_file.name.endswith(".csv")
            else pd.read_excel(policy_file)
        )
        company_policies = df_policy.to_string(index=False)

    st.sidebar.success("Company policies loaded")

# =========================
# EMPLOYEE SELECTION
# =========================
employee_data = None

if employee_df is not None:
    st.sidebar.markdown("### 👤 Select Employee")
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

    left, right = st.columns([1.4, 1.6])

    with left:
        st.markdown("### 📄 Employee Details (Dynamic)")
        st.json(employee_data)

    with right:
        st.markdown("### 🧠 HR Intelligence Query")

        user_query = st.text_area(
            "Ask a policy-aware HR question",
            height=120,
            placeholder="Is this employee eligible for confirmation as per company policy?"
        )

        run_btn = st.button("🔍 Get HR Insight", use_container_width=True)

        if run_btn:
            if not company_policies:
                st.error("❌ Company policies not uploaded")
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
    st.warning("⬅ Upload employee data and policies to begin analysis")



