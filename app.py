import streamlit as st
import pandas as pd
import pdfplumber
from PIL import Image
import pytesseract

from backend import (
    generate_final_hr_report,
    generate_pdf_report
)

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="HR Intelligence Agent", layout="wide")

st.title("🧑‍💼 HR Intelligence Agent")
st.caption("Staffline + Keka + UnlockU → Unified HR Decisions")

# =========================
# LEFT PANEL — BRANDING
# =========================
st.sidebar.image("compunnel_logo.jpg", use_container_width=True)
st.sidebar.header("📥 Upload Portal Data")

# =========================
# STAFFLINE
# =========================
st.sidebar.subheader("🏢 Staffline Portal")

staff_emp_file = st.sidebar.file_uploader(
    "Employee Master Data (CSV / Excel)",
    type=["csv", "xlsx"]
)

policy_file = st.sidebar.file_uploader(
    "Company Policies (PDF / TXT / Image)",
    type=["pdf", "txt", "png", "jpg", "jpeg"]
)

# =========================
# KEKA
# =========================
st.sidebar.subheader("💰 Keka Portal")

keka_file = st.sidebar.file_uploader(
    "Employee Finance Data",
    type=["csv", "xlsx"]
)

# =========================
# UNLOCKU
# =========================
st.sidebar.subheader("📈 UnlockU Portal")

unlocku_file = st.sidebar.file_uploader(
    "Employee Performance Data",
    type=["csv", "xlsx"]
)

# =========================
# LOAD DATA
# =========================
staff_df = keka_df = unlocku_df = None
company_policies = ""

if staff_emp_file:
    staff_df = pd.read_csv(staff_emp_file) if staff_emp_file.name.endswith(".csv") else pd.read_excel(staff_emp_file)
    st.sidebar.success("Employee master loaded")

if policy_file:
    name = policy_file.name.lower()
    if name.endswith(".txt"):
        company_policies = policy_file.read().decode("utf-8")
    elif name.endswith(".pdf"):
        with pdfplumber.open(policy_file) as pdf:
            company_policies = "\n".join(page.extract_text() or "" for page in pdf.pages)
    else:
        company_policies = pytesseract.image_to_string(Image.open(policy_file))

    st.sidebar.success("Company policies loaded")

if keka_file:
    keka_df = pd.read_csv(keka_file) if keka_file.name.endswith(".csv") else pd.read_excel(keka_file)
    st.sidebar.success("Keka finance loaded")

if unlocku_file:
    unlocku_df = pd.read_csv(unlocku_file) if unlocku_file.name.endswith(".csv") else pd.read_excel(unlocku_file)
    st.sidebar.success("UnlockU performance loaded")

# =========================
# EMPLOYEE SELECTION
# =========================
employee_id = None

if staff_df is not None:
    employee_id = st.sidebar.selectbox(
        "Select Employee ID",
        staff_df["employee_id"].astype(str)
    )

# =========================
# MAIN PANEL — HR DECISION
# =========================
if employee_id and staff_df is not None:

    staff_emp = staff_df[staff_df["employee_id"].astype(str) == employee_id].iloc[0].to_dict()

    keka_emp = (
        keka_df[keka_df["employee_id"].astype(str) == employee_id].iloc[0].to_dict()
        if keka_df is not None and employee_id in keka_df["employee_id"].astype(str).values
        else {}
    )

    unlocku_emp = (
        unlocku_df[unlocku_df["employee_id"].astype(str) == employee_id].iloc[0].to_dict()
        if unlocku_df is not None and employee_id in unlocku_df["employee_id"].astype(str).values
        else {}
    )

    st.subheader("🧠 HR Intelligence Query")

    user_query = st.text_area(
        "Ask an HR decision question",
        height=120,
        placeholder="Is this employee eligible for confirmation considering performance and payroll compliance?"
    )

    if st.button("🔍 Generate HR Decision Report", use_container_width=True):

        with st.spinner("Generating HR decision report..."):
            context = {
                "staffline_employee": staff_emp,
                "staffline_policies": company_policies,
                "keka_finance": keka_emp,
                "unlocku_performance": unlocku_emp,
                "user_question": user_query
            }

            final_report = generate_final_hr_report(context)

        st.markdown("### 📑 HR Decision Report")
        st.markdown(final_report)

        pdf_bytes = generate_pdf_report(final_report)

        st.download_button(
            "📥 Download HR Report (PDF)",
            data=pdf_bytes,
            file_name=f"HR_Report_{employee_id}.pdf",
            mime="application/pdf"
        )

else:
    st.info("⬅ Upload all portal data and select an employee")
