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

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(page_title="HR Intelligence Agent", layout="wide")
st.title("🧑‍💼 HR Employee Intelligence Agent")

# =========================
# LEFT PANEL — DATA INGESTION
# =========================
st.sidebar.header("📤 Upload Employee Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"]
)

employee_df = None
employee_data = None

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        employee_df = pd.read_csv(uploaded_file)
    else:
        employee_df = pd.read_excel(uploaded_file)

    st.sidebar.success("Employee data loaded")

    # Employee selector
    emp_id = st.sidebar.selectbox(
        "Select Employee ID",
        employee_df["employee_id"].astype(str)
    )

    employee_data = (
        employee_df[employee_df["employee_id"].astype(str) == emp_id]
        .iloc[0]
        .to_dict()
    )

# =========================
# RIGHT PANEL — DYNAMIC VIEW
# =========================
if employee_data:

    col1, col2 = st.columns([1.2, 1.8])

    # -------------------------
    # Employee Snapshot
    # -------------------------
    with col1:
        st.subheader("📄 Employee Snapshot")
        st.json(employee_data)

    # -------------------------
    # Query + Output
    # -------------------------
    with col2:
        st.subheader("🧠 HR Intelligence Query")

        user_query = st.text_area(
            "Ask any HR-related question about this employee",
            height=120,
            placeholder="e.g. Is this employee eligible for confirmation?"
        )

        analyze_btn = st.button("🔍 Get Result")

        if analyze_btn:
            if not user_query.strip():
                st.warning("Please enter a query before clicking Get Result.")
            else:
                with st.spinner("HR Agent analyzing..."):
                    context = {
                        "employee_data": employee_data,
                        "user_question": user_query
                    }

                    response = generate_ai_explanation(context)

                st.markdown("### 📊 AI Output")
                st.markdown(response)

else:
    st.info("⬅ Upload employee data and select an employee to begin")

