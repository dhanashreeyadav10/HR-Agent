import streamlit as st
import pandas as pd
import pdfplumber
from PIL import Image
import pytesseract

from backend import generate_hr_decision, generate_pdf_report

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="HR Intelligence Agent", layout="wide")

st.title("🧑‍💼 HR Intelligence Agent")
st.caption("Dynamic HR Intelligence – Individual & Organization-wide Analysis")

# =========================
# LEFT PANEL — BRANDING & UPLOADS
# =========================
st.sidebar.image("compunnel_logo.jpg", use_container_width=True)
st.sidebar.header("📥 Upload HR Data")

staff_emp_file = st.sidebar.file_uploader(
    "Employee Master Data (Staffline)",
    type=["csv", "xlsx"]
)

policy_file = st.sidebar.file_uploader(
    "Company Policies (PDF / TXT / Image)",
    type=["pdf", "txt", "png", "jpg", "jpeg"]
)

keka_file = st.sidebar.file_uploader(
    "Employee Finance Data (Keka)",
    type=["csv", "xlsx"]
)

unlocku_file = st.sidebar.file_uploader(
    "Employee Performance Data (UnlockU)",
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
# MAIN PANEL — QUERY (NO EMPLOYEE ID REQUIRED)
# =========================
if staff_df is not None and keka_df is not None and unlocku_df is not None and company_policies:

    st.subheader("🧠 Ask HR Intelligence Questions")

    user_query = st.text_area(
        "Examples:\n• Provide a list of employees likely to leave\n• Who are at payroll risk?\n• Is E1050 eligible for confirmation?",
        height=140
    )

    if st.button("🔍 Run HR Intelligence", use_container_width=True):

        with st.spinner("Analyzing organizational HR data..."):
            context = {
                "staffline_employee_data": staff_df.to_dict(orient="records"),
                "keka_finance_data": keka_df.to_dict(orient="records"),
                "unlocku_performance_data": unlocku_df.to_dict(orient="records"),
                "staffline_policies": company_policies,
                "user_question": user_query
            }

            result = generate_hr_decision(context)

        st.markdown("### 📑 HR Intelligence Result")
        st.markdown(result)

        pdf_bytes = generate_pdf_report(result)

        st.download_button(
            "📥 Download Result as PDF",
            data=pdf_bytes,
            file_name="HR_Intelligence_Report.pdf",
            mime="application/pdf"
        )

else:
    st.info("⬅ Upload all datasets to enable HR Intelligence")
