import streamlit as st
from backend import generate_ai_explanation

st.set_page_config(page_title="HR Agent", layout="wide")

st.title("🧑‍💼 HR Employee Intelligence Agent")

# -------------------------
# Sample Employee Data
# -------------------------
employee_data = {
    "employee_id": 1002,
    "name": "Anita Sharma",
    "employment_type": "Full Time",
    "pan": "ABCDE1234F",
    "bank_account": "SBIN0001234",
    "probation_end_date": "2023-07-10",
    "manager_feedback": "Excellent performance and learning attitude",
    "compliance_status": "READY",
    "missing_items": [],
    "lifecycle_state": "ACTIVE",
    "confirmation_decision": "CONFIRM"
}

# -------------------------
# Display Raw Data
# -------------------------
st.subheader("📄 Employee Record")
st.json(employee_data)

# -------------------------
# Generate AI Explanation
# -------------------------
if st.button("🧠 Generate AI Explanation"):
    with st.spinner("Analyzing employee status..."):
        explanation = generate_ai_explanation(employee_data)

    st.markdown("## 🧠 AI Explanation")
    st.markdown(explanation)
