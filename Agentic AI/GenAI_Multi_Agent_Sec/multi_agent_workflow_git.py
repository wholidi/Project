# multi_agent_workflow.py
from pathlib import Path
from typing import List, Dict, Any

from ai_agent import analyze_path, client, MODEL_NAME  # reuse your setup

# ---------- Agent 1: ScanAgent (already mostly done) ----------

def scan_agent(project_path: Path) -> List[Dict[str, Any]]:
    """
    Uses your existing LLM-powered scanner to analyze all files.
    """
    return analyze_path(project_path)


# ---------- Agent 2: RiskClassifierAgent ----------

RISK_CLASSIFIER_PROMPT = """
You are a security triage expert.

You will receive a JSON array of security findings from another agent.
Each finding has: title, severity, location, description, recommendation, source_file.

Tasks:
1. Normalize `severity` into one of: low, medium, high, critical.
2. (Optional) Add `owasp_category` if you can map it (e.g., A01: Broken Access Control).
3. Do NOT remove any finding. Only enrich or normalize.

Return ONLY a JSON array of findings with the same fields plus optional `owasp_category`.
"""

def risk_classifier_agent(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    import json

    if not findings:
        return []

    response = client.responses.create(
        model=MODEL_NAME,
        instructions=RISK_CLASSIFIER_PROMPT,
        input=[
            {
                "role": "user",
                "content": json.dumps(findings, ensure_ascii=False),
            }
        ],
        max_output_tokens=1500,
    )

    raw = (response.output_text or "").strip()
    # best-effort: if anything goes wrong, just return original findings
    try:
        start = raw.find("[")
        end = raw.rfind("]")
        candidate = raw[start : end + 1] if start != -1 and end != -1 else raw
        enriched = json.loads(candidate)
        if isinstance(enriched, dict):
            enriched = [enriched]
        if isinstance(enriched, list):
            return enriched
    except Exception:
        pass

    return findings


# ---------- Agent 3: SummaryAgent ----------

SUMMARY_PROMPT = """
You are a senior security architect. Create a concise summary of the findings.

Include:
- Overall risk level (low/medium/high/critical) for the project
- 3–5 key issues to fix first
- Any quick wins or hardening recommendations

Return plain text, max ~300 words.
"""

def summary_agent(findings: List[Dict[str, Any]]) -> str:
    import json

    if not findings:
        return "No security issues were detected in the analyzed codebase."

    response = client.responses.create(
        model=MODEL_NAME,
        instructions=SUMMARY_PROMPT,
        input=[
            {
                "role": "user",
                "content": json.dumps(findings, ensure_ascii=False),
            }
        ],
        max_output_tokens=500,
    )

    return (response.output_text or "").strip()


# ---------- Coordinator: run full multi-agent workflow ----------

def run_multi_agent_workflow(project_path: Path) -> Dict[str, Any]:
    """
    Orchestrates the three agents:
      1) ScanAgent      -> raw findings
      2) RiskClassifier -> enriched findings
      3) SummaryAgent   -> human-friendly summary
    """
    raw_findings = scan_agent(project_path)
    classified_findings = risk_classifier_agent(raw_findings)
    summary = summary_agent(classified_findings)

    return {
        "summary": summary,
        "findings": classified_findings,
    }
