# import streamlit as st
# import pandas as pd
# import pdfplumber
# from PIL import Image
# import pytesseract

# from backend import generate_hr_decision, generate_pdf_report

# # -------------------------
# # PAGE CONFIG
# # -------------------------
# st.set_page_config(page_title="HR Intelligence Agent", layout="wide")

# st.title("🧑‍💼 HR Intelligence Agent")
# st.caption("Organization-wide HR Analytics & Decision Intelligence")

# # =========================
# # LEFT PANEL — BRANDING
# # =========================
# st.sidebar.image("compunnel_logo.jpg", use_container_width=True)
# st.sidebar.header("📥 Upload HR Data")

# # =========================
# # FILE UPLOADS
# # =========================
# staff_emp_file = st.sidebar.file_uploader(
#     "Employee Master Data (Staffline)",
#     type=["csv", "xlsx"]
# )

# policy_file = st.sidebar.file_uploader(
#     "Company Policies (PDF / TXT / Image)",
#     type=["pdf", "txt", "png", "jpg", "jpeg"]
# )

# keka_file = st.sidebar.file_uploader(
#     "Employee Finance Data (Keka)",
#     type=["csv", "xlsx"]
# )

# unlocku_file = st.sidebar.file_uploader(
#     "Employee Performance Data (UnlockU)",
#     type=["csv", "xlsx"]
# )

# # =========================
# # LOAD DATA
# # =========================
# staff_df = finance_df = perf_df = None
# company_policies = ""

# if staff_emp_file:
#     staff_df = (
#         pd.read_csv(staff_emp_file)
#         if staff_emp_file.name.endswith(".csv")
#         else pd.read_excel(staff_emp_file)
#     )
#     st.sidebar.success("Employee master loaded")

# if policy_file:
#     name = policy_file.name.lower()
#     if name.endswith(".txt"):
#         company_policies = policy_file.read().decode("utf-8")
#     elif name.endswith(".pdf"):
#         with pdfplumber.open(policy_file) as pdf:
#             company_policies = "\n".join(page.extract_text() or "" for page in pdf.pages)
#     else:
#         company_policies = pytesseract.image_to_string(Image.open(policy_file))
#     st.sidebar.success("Company policies loaded")

# if keka_file:
#     finance_df = (
#         pd.read_csv(keka_file)
#         if keka_file.name.endswith(".csv")
#         else pd.read_excel(keka_file)
#     )
#     st.sidebar.success("Finance data loaded")

# if unlocku_file:
#     perf_df = (
#         pd.read_csv(unlocku_file)
#         if unlocku_file.name.endswith(".csv")
#         else pd.read_excel(unlocku_file)
#     )
#     st.sidebar.success("Performance data loaded")

# # =========================
# # HR ANALYTICS LAYER (CRITICAL)
# # =========================
# def build_hr_signals(staff_df, finance_df, perf_df):
#     merged = (
#         perf_df
#         .merge(staff_df, on="employee_id", how="left")
#         .merge(finance_df, on="employee_id", how="left")
#     )

#     merged["attrition_risk"] = (
#         (merged["performance_status"] == "NEEDS_IMPROVEMENT") |
#         (merged["learning_hours_completed"] < 20) |
#         (merged["bank_verified"] == False)
#     )

#     high_risk = merged[merged["attrition_risk"] == True]

#     signals = {
#         "total_employees": len(staff_df),
#         "high_attrition_risk_count": len(high_risk),
#         "high_risk_sample": high_risk[
#             ["employee_id", "department", "performance_status", "learning_hours_completed"]
#         ].head(15).to_dict(orient="records"),
#         "department_risk_distribution": (
#             high_risk["department"].value_counts().head(5).to_dict()
#         )
#     }

#     return signals

# # =========================
# # MAIN PANEL — DYNAMIC HR CHAT
# # =========================
# if staff_df is not None and finance_df is not None and perf_df is not None and company_policies:

#     st.subheader("🧠 Ask HR Intelligence Questions")

#     user_query = st.text_area(
#         "Examples:\n"
#         "• Provide a list of employees likely to leave the company\n"
#         "• Which departments are at highest attrition risk?\n"
#         "• How many employees need HR intervention?",
#         height=140
#     )

#     if st.button("🔍 Run HR Intelligence", use_container_width=True):

#         with st.spinner("Analyzing HR signals..."):
#             hr_signals = build_hr_signals(staff_df, finance_df, perf_df)

#             context = {
#                 "hr_signals": hr_signals,
#                 "company_policies": company_policies,
#                 "user_question": user_query
#             }

#             result = generate_hr_decision(context)

#         st.markdown("### 📑 HR Intelligence Result")
#         st.markdown(result)

#         pdf_bytes = generate_pdf_report(result)

#         st.download_button(
#             "📥 Download Result as PDF",
#             data=pdf_bytes,
#             file_name="HR_Intelligence_Report.pdf",
#             mime="application/pdf"
#         )

# else:
#     st.info("⬅ Upload all datasets to enable HR Intelligence")

import streamlit as st
import pandas as pd
import pdfplumber
from PIL import Image
import pytesseract

from backend import generate_hr_decision, generate_pdf_report

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Core Employee Management",
    layout="wide"
)

st.title("🧑‍💼 Core Employee Management")
st.caption("Organization-wide HR Analytics & Decision Intelligence")

# =========================
# SIDEBAR — BRANDING
# =========================
st.sidebar.image("compunnel_logo.jpg", use_container_width=True)
st.sidebar.header("📥 Upload HR Data")

# =========================
# FILE UPLOADS
# =========================
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
staff_df = finance_df = perf_df = None
company_policies = ""

if staff_emp_file:
    staff_df = (
        pd.read_csv(staff_emp_file)
        if staff_emp_file.name.endswith(".csv")
        else pd.read_excel(staff_emp_file)
    )
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
    finance_df = (
        pd.read_csv(keka_file)
        if keka_file.name.endswith(".csv")
        else pd.read_excel(keka_file)
    )
    st.sidebar.success("Finance data loaded")

if unlocku_file:
    perf_df = (
        pd.read_csv(unlocku_file)
        if unlocku_file.name.endswith(".csv")
        else pd.read_excel(unlocku_file)
    )
    st.sidebar.success("Performance data loaded")

# =========================
# HR SIGNAL ENGINE
# =========================
def build_hr_signals(staff_df, finance_df, perf_df):
    merged = (
        perf_df
        .merge(staff_df, on="employee_id", how="left")
        .merge(finance_df, on="employee_id", how="left")
    )

    merged["attrition_risk"] = (
        (merged["performance_status"] == "NEEDS_IMPROVEMENT")
        | (merged["learning_hours_completed"] < 20)
        | (merged["bank_verified"] == False)
    )

    high_risk = merged[merged["attrition_risk"] == True]

    return {
        "total_employees": len(staff_df),
        "high_attrition_risk_count": len(high_risk),
        "high_risk_sample": high_risk[
            ["employee_id", "department", "performance_status", "learning_hours_completed"]
        ].head(15).to_dict(orient="records"),
        "department_risk_distribution": high_risk["department"].value_counts().to_dict()
    }

# =========================
# MAIN PANEL — HR INTELLIGENCE
# =========================
if staff_df is not None and finance_df is not None and perf_df is not None and company_policies:

    st.subheader("🧠 Ask HR Intelligence Questions")

    user_query = st.text_area(
        "Example questions:\n"
        "• Which employees are at high attrition risk?\n"
        "• Which departments need HR intervention?\n"
        "• Summarize workforce risks for leadership",
        height=140
    )

    if st.button("🔍 Run HR Intelligence", use_container_width=True):

        with st.spinner("Analyzing HR signals..."):
            hr_signals = build_hr_signals(staff_df, finance_df, perf_df)

            context = {
                "hr_signals": hr_signals,
                "company_policies": company_policies,
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

