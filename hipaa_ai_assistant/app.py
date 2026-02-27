# app.py
import streamlit as st
import pandas as pd

from hipaa_questions import questions_core, questions_full
from risk_engine import generate_risk_report
from pdf_export import build_hipaa_pdf


def safe_filename(text: str) -> str:
    text = (text or "organization").strip().replace(" ", "_")
    # keep it simple for Windows filenames
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    return "".join(ch for ch in text if ch in allowed) or "organization"


st.set_page_config(page_title="Complisstant", layout="wide")

st.title("Complisstant")
st.caption("Your virtual compliance analyst for HIPAA Security Risk Assessments (SRA).")

# -----------------------------
# Org Info
# -----------------------------
st.subheader("Organization Info")
org_name = st.text_input("Organization Name", value="")
org_type = st.selectbox("Organization Type", ["Clinic (20–150)", "Rural Hospital", "Other"])
employees = st.selectbox("Employees", ["20-50", "50-100", "100-150"])
uses_msp = st.selectbox("Do you use an MSP?", ["Yes", "No", "Unsure"])

org_context = {
    "organization": org_name,
    "type": org_type,
    "employees": employees,
    "uses_msp": uses_msp,
}

st.divider()

# -----------------------------
# Assessment Mode
# -----------------------------
st.subheader("Assessment")
assessment_mode = st.selectbox(
    "Assessment Mode",
    ["Basic (Core 20)", "Advanced (Full Security Rule)"]
)

selected_questions = questions_core if assessment_mode.startswith("Basic") else questions_full

if assessment_mode.startswith("Advanced"):
    st.info("Advanced mode includes full HIPAA Security Rule coverage and may take longer to complete.")

use_ai_polish = st.checkbox("Use AI to polish findings (recommended)", value=True)

st.divider()

# -----------------------------
# Questionnaire
# -----------------------------
st.subheader("HIPAA Security Rule Questionnaire")

responses = {}
for q in selected_questions:
    responses[q["id"]] = st.selectbox(
        f"{q['question']}  ({q['citation']} • {q['required']})",
        ["Yes", "No", "Unsure"],
        key=q["id"]
    )

# -----------------------------
# Generate
# -----------------------------
if st.button("Generate Dashboard + Report"):
    with st.spinner("Generating dashboard..."):
        summary, findings, overall_level, score_breakdown = generate_risk_report(
            org_context=org_context,
            questions=selected_questions,
            responses=responses,
            use_ai_polish=use_ai_polish
        )

    # ---- DASHBOARD KPIs ----
    overall_score = score_breakdown.get("Overall", 0.0)
    high_findings = sum(1 for f in findings if f.get("risk_level") == "High")
    med_findings = sum(1 for f in findings if f.get("risk_level") == "Medium")
    low_findings = sum(1 for f in findings if f.get("risk_level") == "Low")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("HIPAA Compliance Score", f"{overall_score}%")
    c2.metric("Overall Risk Level", overall_level)
    c3.metric("Total Findings", str(len(findings)))
    c4.metric("High / Med / Low", f"{high_findings} / {med_findings} / {low_findings}")

    st.progress(min(max(int(overall_score), 0), 100))

    st.divider()

    # ---- CATEGORY SCORE CHART ----
    st.subheader("Compliance Score by Safeguard Category")
    cat_rows = [{"Category": k, "Score (%)": v} for k, v in score_breakdown.items() if k != "Overall"]
    df_scores = pd.DataFrame(cat_rows).sort_values("Score (%)", ascending=False)

    if not df_scores.empty:
        st.bar_chart(df_scores.set_index("Category"))
    else:
        st.info("No category scoring data available.")

    st.divider()

    # ---- SUMMARY ----
    st.subheader("Executive Summary")
    st.write(summary)

    # ---- FINDINGS ----
    st.subheader("Findings")
    if not findings:
        st.info("No findings were triggered based on responses.")
    else:
        # Sort findings: High -> Medium -> Low, then by score desc
        order = {"High": 0, "Medium": 1, "Low": 2}
        findings_sorted = sorted(
            findings,
            key=lambda f: (order.get(f.get("risk_level", "Low"), 3), -(f.get("score", 0)))
        )

        for f in findings_sorted:
            with st.expander(f"({f['risk_level']}) {f['title']} — {f['citation']}"):
                st.write(f"**Category:** {f.get('category','N/A')}")
                st.write(f"**Required/Addressable:** {f.get('required','N/A')}")
                st.write(f"**Observation:** {f.get('observation','N/A')}")
                st.write(f"**Recommendation:** {f.get('recommendation','N/A')}")
                st.write(f"**Likelihood:** {f.get('likelihood','N/A')}  |  **Impact:** {f.get('impact','N/A')}  |  **Score:** {f.get('score','N/A')}")

    st.divider()

    # ---- PDF EXPORT ----
    pdf_bytes = build_hipaa_pdf(
        org_context=org_context,
        summary=summary,
        overall_level=overall_level,
        findings=findings
    )

    filename = f"Complisstant_HIPAA_SRA_{safe_filename(org_context.get('organization'))}.pdf"

    st.download_button(
        label="Download PDF Report",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf"
    )