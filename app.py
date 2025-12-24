# import streamlit as st
# import pandas as pd
# import pdfplumber
# from PIL import Image
# import pytesseract
# from backend import generate_ai_explanation

# # -------------------------
# # PAGE CONFIG
# # -------------------------
# st.set_page_config(
#     page_title="HR Knowledge-Based Intelligence Agent",
#     layout="wide"
# )

# st.title("🧑‍💼 HR Knowledge-Based Intelligence Agent")
# st.caption("Employee data + Company policies → Policy-aware HR insights")

# # =========================
# # LEFT PANEL — BRANDING
# # =========================
# st.sidebar.image(
#     "compunnel_logo.jpg",
#     use_container_width=True
# )

# st.sidebar.header("📥 Knowledge Base Upload")

# # =========================
# # UPLOAD FILES
# # =========================
# emp_file = st.sidebar.file_uploader(
#     "Upload Employee Data (CSV / Excel)",
#     type=["csv", "xlsx"]
# )

# policy_file = st.sidebar.file_uploader(
#     "Upload Company Policy (PDF / TXT / Image)",
#     type=["pdf", "txt", "png", "jpg", "jpeg"]
# )

# employee_df = None
# employee_data = None
# company_policies = ""

# # -------------------------
# # LOAD EMPLOYEE DATA
# # -------------------------
# if emp_file:
#     employee_df = (
#         pd.read_csv(emp_file)
#         if emp_file.name.endswith(".csv")
#         else pd.read_excel(emp_file)
#     )
#     st.sidebar.success("Employee data loaded")

# # -------------------------
# # LOAD POLICY DATA
# # -------------------------
# if policy_file:
#     try:
#         name = policy_file.name.lower()

#         if name.endswith(".txt"):
#             company_policies = policy_file.read().decode("utf-8")

#         elif name.endswith(".pdf"):
#             with pdfplumber.open(policy_file) as pdf:
#                 company_policies = "\n".join(
#                     page.extract_text() or "" for page in pdf.pages
#                 )

#         elif name.endswith((".png", ".jpg", ".jpeg")):
#             image = Image.open(policy_file)
#             company_policies = pytesseract.image_to_string(image)

#         st.sidebar.success("Company policy loaded")

#     except Exception as e:
#         st.sidebar.error(f"Policy extraction failed: {e}")

# # =========================
# # EMPLOYEE SELECTION
# # =========================
# if employee_df is not None:
#     st.sidebar.subheader("👤 Select Employee")

#     emp_id = st.sidebar.selectbox(
#         "Employee ID",
#         employee_df["employee_id"].astype(str)
#     )

#     employee_data = (
#         employee_df[employee_df["employee_id"].astype(str) == emp_id]
#         .iloc[0]
#         .to_dict()
#     )

#     # Minimal info only (no JSON on main screen)
#     st.sidebar.markdown(
#         f"""
#         **Name:** {employee_data.get('name', 'N/A')}  
#         **Department:** {employee_data.get('department', 'N/A')}  
#         **Status:** {employee_data.get('employment_status', 'N/A')}
#         """
#     )

# # =========================
# # RIGHT PANEL — QUERY & OUTPUT
# # =========================
# if employee_data:

#     st.subheader("🧠 HR Intelligence Query")

#     user_query = st.text_area(
#         "Ask a policy-aware HR question",
#         height=120,
#         placeholder="Is this employee eligible for WFH as per company policy?"
#     )

#     if st.button("🔍 Get HR Insight", use_container_width=True):

#         if not company_policies.strip():
#             st.error("❌ Please upload company policy")
#         elif not user_query.strip():
#             st.error("❌ Please enter a question")
#         else:
#             with st.spinner("Analyzing employee data & policies..."):
#                 context = {
#                     "employee_data": employee_data,      # hidden
#                     "company_policies": company_policies,
#                     "user_question": user_query
#                 }

#                 response = generate_ai_explanation(context)

#             st.markdown("### 📊 AI Output")
#             st.markdown(response)

# else:
#     st.info("⬅ Upload employee data and company policy to begin")









import streamlit as st
import pandas as pd
import pdfplumber
from PIL import Image
import pytesseract
from backend import generate_ai_explanation

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="HR Intelligence Agent", layout="wide")

st.title("🧑‍💼 HR Intelligence Agent")
st.caption("Staffline + Keka + UnlockU → Unified HR Intelligence")

# =========================
# LEFT PANEL — BRANDING
# =========================
st.sidebar.image("compunnel_logo.jpg", use_container_width=True)

st.sidebar.header("📥 Upload Portal Data")

# =========================
# STAFFLINE UPLOADS
# =========================
st.sidebar.subheader("🏢 Staffline Portal")

staff_emp_file = st.sidebar.file_uploader(
    "Employee Master Data (CSV / Excel)",
    type=["csv", "xlsx"]
)

staff_policy_file = st.sidebar.file_uploader(
    "Company Policies (PDF / TXT / Image)",
    type=["pdf", "txt", "png", "jpg", "jpeg"]
)

# =========================
# KEKA UPLOAD
# =========================
st.sidebar.subheader("💰 Keka Portal")

keka_file = st.sidebar.file_uploader(
    "Employee Finance / Payroll Data",
    type=["csv", "xlsx"]
)

# =========================
# UNLOCKU UPLOAD
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

# Staffline employee
if staff_emp_file:
    staff_df = (
        pd.read_csv(staff_emp_file)
        if staff_emp_file.name.endswith(".csv")
        else pd.read_excel(staff_emp_file)
    )
    st.sidebar.success("Staffline employee data loaded")

# Policies
if staff_policy_file:
    name = staff_policy_file.name.lower()

    if name.endswith(".txt"):
        company_policies = staff_policy_file.read().decode("utf-8")

    elif name.endswith(".pdf"):
        with pdfplumber.open(staff_policy_file) as pdf:
            company_policies = "\n".join(
                page.extract_text() or "" for page in pdf.pages
            )

    else:
        image = Image.open(staff_policy_file)
        company_policies = pytesseract.image_to_string(image)

    st.sidebar.success("Company policies loaded")

# Keka
if keka_file:
    keka_df = (
        pd.read_csv(keka_file)
        if keka_file.name.endswith(".csv")
        else pd.read_excel(keka_file)
    )
    st.sidebar.success("Keka finance data loaded")

# UnlockU
if unlocku_file:
    unlocku_df = (
        pd.read_csv(unlocku_file)
        if unlocku_file.name.endswith(".csv")
        else pd.read_excel(unlocku_file)
    )
    st.sidebar.success("UnlockU performance data loaded")

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
# RIGHT PANEL — QUERY
# =========================
if employee_id and staff_df is not None:

    staff_emp = staff_df[
        staff_df["employee_id"].astype(str) == employee_id
    ].iloc[0].to_dict()

    keka_emp = (
        keka_df[keka_df["employee_id"].astype(str) == employee_id]
        .iloc[0].to_dict()
        if keka_df is not None and employee_id in keka_df["employee_id"].astype(str).values
        else {}
    )

    unlocku_emp = (
        unlocku_df[unlocku_df["employee_id"].astype(str) == employee_id]
        .iloc[0].to_dict()
        if unlocku_df is not None and employee_id in unlocku_df["employee_id"].astype(str).values
        else {}
    )

    st.subheader("🧠 HR Intelligence Query")

    user_query = st.text_area(
        "Ask a cross-system HR question",
        height=120,
        placeholder="Is this employee eligible for confirmation considering performance and payroll compliance?"
    )

    if st.button("🔍 Get HR Insight", use_container_width=True):

        if not company_policies:
            st.error("Company policies missing (Staffline)")
        else:
            with st.spinner("Correlating Staffline + Keka + UnlockU data..."):
                context = {
                    "staffline_employee": staff_emp,
                    "staffline_policies": company_policies,
                    "keka_finance": keka_emp,
                    "unlocku_performance": unlocku_emp,
                    "user_question": user_query
                }

                response = generate_ai_explanation(context)

            st.markdown("### 📊 AI Output")
            st.markdown(response)

else:
    st.info("⬅ Upload all portal data and select an employee")
