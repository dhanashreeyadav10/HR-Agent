import streamlit as st
import pandas as pd
from backend import run_hr_system

st.set_page_config(layout="wide")
st.title("🏢 HR Core Employee Management System")

uploaded = st.file_uploader("Upload Employee Data (CSV / Excel)", ["csv", "xlsx"])

if uploaded:
    df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)

    results = run_hr_system(df)

    master = results["master"]
    cases = results["case_file"]
    explain_agent = results["explain_agent"]

    # ------------------ MASTER SUMMARY ------------------
    st.subheader("📊 Employee Master Health")
    st.json(master)

    # ------------------ EMPLOYEE 360 ------------------
    st.subheader("👤 Employee 360° Case File")
    emp_id = st.selectbox("Select Employee ID", cases["employee_id"].unique())
    emp_case = cases[cases["employee_id"] == emp_id].iloc[0]

    st.json(emp_case.to_dict())

    st.subheader("🧠 AI Explanation")
    st.text(explain_agent.explain(emp_case))
