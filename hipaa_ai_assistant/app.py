# app.py
import streamlit as st
import pandas as pd

from hipaa_questions import questions_core, questions_full
from risk_engine import generate_risk_report
from pdf_export import build_hipaa_pdf


def safe_filename(text: str) -> str:
    text = (text or "organization").strip().replace(" ", "_")
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    return "".join(ch for ch in text if ch in allowed) or "organization"


def risk_badge(level: str) -> str:
    if level == "High":
        return "badge-high"
    if level == "Medium":
        return "badge-med"
    return "badge-low"


st.set_page_config(page_title="Complisstant", layout="wide")

# -----------------------------
# ELECTRIC BLUE DARK STYLING
# -----------------------------
st.markdown("""
<style>
.block-container { padding-top: 1.5rem; max-width: 1200px; }

/* Header */
.ca-header {
  border-radius: 20px;
  padding: 20px 24px;
  background: linear-gradient(90deg, #0B1220 0%, #0f1b36 40%, #001F3F 100%);
  border: 1px solid rgba(0,191,255,0.25);
  box-shadow: 0 0 40px rgba(0,191,255,0.08);
}
.ca-header h1 {
  margin: 0;
  font-size: 30px;
  color: #00BFFF;
  letter-spacing: 1px;
}
.ca-header p {
  margin: 6px 0 0 0;
  color: #9CA3AF;
}

/* Section Titles */
.section-title {
  margin-top: 22px;
  font-weight: 700;
  font-size: 15px;
  color: #00BFFF;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* KPI Cards */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-top: 12px;
}

.card {
  background: #111827;
  border-radius: 18px;
  padding: 16px;
  border: 1px solid rgba(0,191,255,0.15);
  box-shadow: 0 0 25px rgba(0,191,255,0.05);
}

.card .label {
  font-size: 12px;
  color: #9CA3AF;
}

.card .value {
  font-size: 24px;
  font-weight: 800;
  margin-top: 4px;
  color: #00BFFF;
}

.card .sub {
  margin-top: 6px;
  font-size: 12px;
  color: #6B7280;
}

/* Risk Badges */
.badge {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
}

.badge-high {
  background: rgba(220,38,38,0.15);
  color: #EF4444;
  border: 1px solid rgba(220,38,38,0.35);
}

.badge-med {
  background: rgba(245,158,11,0.15);
  color: #F59E0B;
  border: 1px solid rgba(245,158,11,0.35);
}

.badge-low {
  background: rgba(34,197,94,0.15);
  color: #22C55E;
  border: 1px solid rgba(34,197,94,0.35);
}

/* Buttons */
.stButton>button {
  background: #00BFFF;
  color: black;
  font-weight: 700;
  border-radius: 14px;
  border: none;
}
.stButton>button:hover {
  background: #1ecfff;
}

/* Progress bar glow */
.stProgress > div > div > div > div {
  background-color: #00BFFF;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="ca-header">
  <h1>Complisstant</h1>
  <p>AI-powered HIPAA Security Risk Assessment platform for healthcare organizations.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="section-title">Organization Info</div>', unsafe_allow_html=True)
    org_name = st.text_input("Organization Name")
    org_type = st.selectbox("Organization Type", ["Clinic (20–150)", "Rural Hospital", "Other"])
    employees = st.selectbox("Employees", ["20-50", "50-100", "100-150"])
    uses_msp = st.selectbox("Do you use an MSP?", ["Yes", "No", "Unsure"])

    st.markdown('<div class="section-title">Assessment Settings</div>', unsafe_allow_html=True)
    assessment_mode = st.selectbox("Assessment Mode", ["Basic (Core 20)", "Advanced (Full Security Rule)"])
    selected_questions = questions_core if assessment_mode.startswith("Basic") else questions_full
    use_ai_polish = st.checkbox("Use AI to polish findings", value=True)

with right:
    st.markdown('<div class="section-title">Questionnaire</div>', unsafe_allow_html=True)
    responses = {}
    for q in selected_questions:
        responses[q["id"]] = st.selectbox(
            f"{q['question']} ({q['citation']})",
            ["Yes", "No", "Unsure"],
            key=q["id"]
        )

st.divider()

if st.button("Generate Dashboard + Report"):
    summary, findings, overall_level, score_breakdown = generate_risk_report(
        org_context={
            "organization": org_name,
            "type": org_type,
            "employees": employees,
            "uses_msp": uses_msp,
        },
        questions=selected_questions,
        responses=responses,
        use_ai_polish=use_ai_polish
    )

    overall_score = score_breakdown.get("Overall", 0)

    st.markdown('<div class="section-title">Dashboard</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="kpi-row">
        <div class="card">
            <div class="label">Compliance Score</div>
            <div class="value">{overall_score}%</div>
            <div class="sub">Weighted across controls</div>
        </div>
        <div class="card">
            <div class="label">Overall Risk</div>
            <div class="value">{overall_level}</div>
            <div class="sub">Highest triggered finding</div>
        </div>
        <div class="card">
            <div class="label">Total Findings</div>
            <div class="value">{len(findings)}</div>
            <div class="sub">Based on responses</div>
        </div>
        <div class="card">
            <div class="label">Assessment Mode</div>
            <div class="value">{assessment_mode.split()[0]}</div>
            <div class="sub">Coverage depth</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(int(overall_score))

    st.divider()

    st.markdown('<div class="section-title">Findings</div>', unsafe_allow_html=True)

    for f in findings:
        badge_class = risk_badge(f["risk_level"])
        st.markdown(
            f'<span class="badge {badge_class}">{f["risk_level"]}</span> '
            f'<b>{f["title"]}</b> ({f["citation"]})',
            unsafe_allow_html=True
        )
        st.write(f"**Observation:** {f['observation']}")
        st.write(f"**Recommendation:** {f['recommendation']}")
        st.write("---")

    pdf_bytes = build_hipaa_pdf(
        org_context={"organization": org_name},
        summary=summary,
        overall_level=overall_level,
        findings=findings
    )

    st.download_button(
        "Download PDF Report",
        pdf_bytes,
        file_name=f"Complisstant_HIPAA_SRA_{safe_filename(org_name)}.pdf",
        mime="application/pdf"
    )