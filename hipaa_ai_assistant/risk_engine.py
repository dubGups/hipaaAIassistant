from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ANSWER_FACTOR = {
    "Yes": 1.0,
    "Unsure": 0.5,
    "No": 0.0
}

def score_to_level(score: int) -> str:
    if score <= 3:
        return "Low"
    if score <= 6:
        return "Medium"
    return "High"

def build_rule_findings(questions, responses):
    findings = []
    for q in questions:
        answer = responses.get(q["id"])
        if answer in q.get("trigger_if", []):
            likelihood = int(q.get("default_likelihood", 2))
            impact = int(q.get("default_impact", 2))
            score = likelihood * impact
            findings.append({
                "id": q["id"],
                "category": q.get("category", "Uncategorized"),
                "title": q["finding_title"],
                "citation": q["citation"],
                "answer": answer,
                "likelihood": likelihood,
                "impact": impact,
                "score": score,
                "risk_level": score_to_level(score),
                "recommendation": q["recommendation"],
                "observation": f"Response was '{answer}' for: {q['question']}"
            })
    return findings

def ai_polish_findings(org_context: dict, findings: list[dict]) -> list[dict]:
    if not findings:
        return findings

    prompt = f"""
You are a HIPAA Security Rule assessor. Rewrite each finding below to be audit-ready.
Keep:
- title, citation, likelihood, impact, score, risk_level, category
Improve:
- observation (2-3 sentences)
- recommendation (actionable, concise)

Organization context:
{org_context}

Findings:
{findings}

Return JSON in the format: {{"findings":[...]}} with the same keys for each finding.
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You write audit-ready HIPAA risk assessment findings."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"}
    )

    import json
    parsed = json.loads(resp.choices[0].message.content)
    return parsed.get("findings", findings)

def compute_compliance_scores(questions, responses):
    """
    Weighted score:
      Yes = 100% of weight
      Unsure = 50% of weight
      No = 0% of weight
    """
    totals = {"Overall": {"earned": 0.0, "possible": 0.0}}
    for q in questions:
        cat = q.get("category", "Uncategorized")
        weight = float(q.get("weight", 1))
        ans = responses.get(q["id"], "Unsure")
        factor = ANSWER_FACTOR.get(ans, 0.5)

        if cat not in totals:
            totals[cat] = {"earned": 0.0, "possible": 0.0}

        totals[cat]["earned"] += weight * factor
        totals[cat]["possible"] += weight

        totals["Overall"]["earned"] += weight * factor
        totals["Overall"]["possible"] += weight

    # Convert to percentages
    percentages = {}
    for cat, v in totals.items():
        possible = v["possible"] or 1.0
        percentages[cat] = round((v["earned"] / possible) * 100, 1)

    return percentages

def generate_risk_report(org_context: dict, questions: list[dict], responses: dict, use_ai_polish: bool = True):
    findings = build_rule_findings(questions, responses)

    if use_ai_polish and findings:
        findings = ai_polish_findings(org_context, findings)

    overall_score = max([f["score"] for f in findings], default=1)
    overall_level = score_to_level(overall_score)

    score_breakdown = compute_compliance_scores(questions, responses)
    overall_compliance = score_breakdown.get("Overall", 0.0)

    summary = (
        f"**HIPAA Compliance Score:** {overall_compliance}%\n\n"
        f"**Overall Risk Level:** {overall_level} (highest finding score: {overall_score})\n\n"
        f"**Total Findings Identified:** {len(findings)}"
    )

    return summary, findings, overall_level, score_breakdown