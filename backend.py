import os
import pandas as pd
from dotenv import load_dotenv

# Optional Groq
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except:
    GROQ_AVAILABLE = False

load_dotenv()

# =====================================================
# CANONICAL HR MAPPER
# =====================================================
def canonicalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.lower().strip() for c in df.columns]

    def col(name):
        return df[name] if name in df.columns else None

    return pd.DataFrame({
        "employee_id": col("employee_id"),
        "name": col("name"),
        "gender": col("gender"),
        "date_of_joining": col("date_of_joining"),
        "employment_status": col("employment_status"),
        "department": col("department"),
        "designation": col("designation"),
        "manager_id": col("manager_id"),
        "employment_type": col("employment_type"),
        "pan": col("pan"),
        "bank_account": col("bank_account"),
        "probation_end_date": col("probation_end_date"),
        "manager_feedback": col("manager_feedback")
    })


# =====================================================
# EMPLOYEE MASTER AGENT
# =====================================================
class EmployeeMasterAgent:
    def evaluate(self, df):
        issues = []
        if df["employee_id"].isnull().any():
            issues.append("Missing Employee ID")
        if df["employee_id"].duplicated().any():
            issues.append("Duplicate Employee ID")

        return {
            "status": "VALID" if not issues else "INVALID",
            "issues": issues,
            "total_employees": df["employee_id"].nunique()
        }


# =====================================================
# COMPLIANCE AGENT
# =====================================================
class ComplianceAgent:
    def evaluate(self, df):
        rows = []
        for _, r in df.iterrows():
            missing = []
            if pd.isna(r["pan"]):
                missing.append("PAN")
            if pd.isna(r["bank_account"]):
                missing.append("Bank Account")

            rows.append({
                "employee_id": r["employee_id"],
                "compliance_status": "READY" if not missing else "BLOCKED",
                "missing_items": missing
            })
        return pd.DataFrame(rows)


# =====================================================
# LIFECYCLE AGENT
# =====================================================
class LifecycleAgent:
    def evaluate(self, df):
        rows = []
        for _, r in df.iterrows():
            status = str(r["employment_status"]).lower()
            if status == "active":
                state = "ACTIVE"
            elif status in ["resigned", "exit", "exited"]:
                state = "EXIT"
            else:
                state = "ONBOARDING"

            rows.append({
                "employee_id": r["employee_id"],
                "lifecycle_state": state
            })
        return pd.DataFrame(rows)


# =====================================================
# CONFIRMATION AGENT
# =====================================================
class ConfirmationAgent:
    def evaluate(self, df):
        today = pd.Timestamp.today()
        rows = []

        for _, r in df.iterrows():
            if pd.isna(r["probation_end_date"]):
                decision = "NOT_APPLICABLE"
            else:
                end = pd.to_datetime(r["probation_end_date"], errors="coerce")
                if end and end > today:
                    decision = "IN_PROGRESS"
                else:
                    fb = str(r["manager_feedback"]).lower()
                    decision = "CONFIRM" if any(x in fb for x in ["good", "excellent", "strong"]) else "REVIEW"

            rows.append({
                "employee_id": r["employee_id"],
                "confirmation_decision": decision
            })
        return pd.DataFrame(rows)


# =====================================================
# EXPLAINABILITY AGENT
# =====================================================
class ExplainabilityAgent:
    def __init__(self):
        self.use_groq = GROQ_AVAILABLE and os.getenv("GROQ_API_KEY")
        if self.use_groq:
            self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def explain(self, row):
        if self.use_groq:
            prompt = f"""
Explain this employee case for HR:

Employee ID: {row['employee_id']}
Lifecycle: {row['lifecycle_state']}
Compliance: {row['compliance_status']}
Confirmation: {row['confirmation_decision']}
"""
            try:
                resp = self.client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                return resp.choices[0].message.content
            except:
                pass

        return (
            "Employee requires HR action due to pending compliance or confirmation. "
            "Recommended steps: complete documents and manager review."
        )


# =====================================================
# ORCHESTRATOR
# =====================================================
def run_hr_system(uploaded_df: pd.DataFrame):
    df = canonicalize(uploaded_df)

    master = EmployeeMasterAgent().evaluate(df)
    compliance = ComplianceAgent().evaluate(df)
    lifecycle = LifecycleAgent().evaluate(df)
    confirmation = ConfirmationAgent().evaluate(df)
    explain_agent = ExplainabilityAgent()

    case_file = (
        df.merge(compliance, on="employee_id", how="left")
          .merge(lifecycle, on="employee_id", how="left")
          .merge(confirmation, on="employee_id", how="left")
    )

    return {
        "master": master,
        "case_file": case_file,
        "explain_agent": explain_agent
    }
