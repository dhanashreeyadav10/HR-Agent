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
from backend import generate_ai_explanation

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="HR AI Chatbot", layout="wide")
st.title("🧑‍💼 HR Employee Intelligence Chatbot")

# -------------------------
# Static Employee Data (can later come from CSV/API)
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
# Sidebar – Employee Context
# -------------------------
with st.sidebar:
    st.header("📄 Employee Context")
    st.json(employee_data)
    st.markdown(
        """
        This data is used as **context** for the HR AI Agent.
        Ask any HR-related question about this employee.
        """
    )

# -------------------------
# Session State for Chat
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# Display Chat History
# -------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# Chat Input
# -------------------------
user_query = st.chat_input("Ask anything about this employee...")

if user_query:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_query}
    )
    with st.chat_message("user"):
        st.markdown(user_query)

    # AI Response
    with st.chat_message("assistant"):
        with st.spinner("HR Agent analyzing..."):
            # Combine user question + employee data
            prompt_employee = {
                "employee_data": employee_data,
                "user_question": user_query
            }

            response = generate_ai_explanation(prompt_employee)

        st.markdown(response)

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )


