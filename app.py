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

st.set_page_config(page_title="HR Intelligence Chatbot", layout="wide")
st.title("🧑‍💼 HR Employee Intelligence Agent")

# -------------------------
# Upload HR Data
# -------------------------
st.sidebar.header("📤 Upload Employee Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

employee_df = None

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        employee_df = pd.read_csv(uploaded_file)
    else:
        employee_df = pd.read_excel(uploaded_file)

    st.sidebar.success("Employee data loaded successfully")

# -------------------------
# Select Employee
# -------------------------
employee_data = None

if employee_df is not None:
    emp_id = st.sidebar.selectbox(
        "Select Employee ID",
        employee_df["employee_id"].astype(str)
    )

    employee_data = (
        employee_df[employee_df["employee_id"].astype(str) == emp_id]
        .iloc[0]
        .to_dict()
    )

    st.sidebar.subheader("📄 Employee Context")
    st.sidebar.json(employee_data)

# -------------------------
# Chat Session
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# Chat Input
# -------------------------
if employee_data:
    user_query = st.chat_input("Ask HR questions about the selected employee")

    if user_query:
        st.session_state.messages.append(
            {"role": "user", "content": user_query}
        )
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("HR Agent analyzing..."):
                context = {
                    "employee_data": employee_data,
                    "user_question": user_query
                }
                response = generate_ai_explanation(context)

            st.markdown(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
else:
    st.info("⬅ Upload employee data and select an employee to start chatting")

