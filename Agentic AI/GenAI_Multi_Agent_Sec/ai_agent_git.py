from pathlib import Path
import json
import os
from typing import List, Dict, Any

from dotenv import load_dotenv
from openai import OpenAI

from report_html import save_html_report  # <-- use your HTML helper


# ----------------------------------------------------------
# Load env + endpoint 
# please setup endpoint or direct API key 
# ----------------------------------------------------------
load_dotenv()

client = OpenAI(
    base_url="https://end-point.com/",
    api_key=os.getenv("OPENAI_API_KEY"),
)

MODEL_NAME = "o3-mini"
INCLUDE_EXTENSIONS = {".py", ".js", ".ts", ".java", ".cs", ".go"}


SECURITY_INSTRUCTIONS = """
You are a senior application security engineer performing a STRICT security review.

The code you receive MAY contain vulnerabilities. You MUST actively look for issues, especially:

- SQL, NoSQL, command or LDAP injection
- XSS / HTML injection
- Authentication and authorization weaknesses
- Hardcoded secrets / credentials / tokens
- Insecure cryptography and random number generation
- Insecure file handling, deserialization, or use of eval/exec
- Logging or exposing sensitive data
- Any other OWASP-style vulnerability

Rules:
- Treat ALL external / user input as UNTRUSTED by default.
- If untrusted data is concatenated into a SQL query string,
  this MUST be flagged as HIGH severity SQL Injection.
- If ANY possible vulnerability exists, you MUST report it.
- Only return [] if the code is genuinely safe.

Output format:
Return ONLY a JSON array. Each element MUST be an object with:
- title
- severity ("low", "medium", "high", "critical")
- location
- description
- recommendation
"""


# --------------------- single file ------------------------
def analyze_file(file_path: Path) -> List[Dict[str, Any]]:
    code = file_path.read_text(encoding="utf-8", errors="ignore")

    response = client.responses.create(
        model=MODEL_NAME,
        instructions=SECURITY_INSTRUCTIONS,
        input=[
            {
                "role": "user",
                "content": (
                    f"Perform a security review of this file.\n"
                    f"File: {file_path}\n\n"
                    f"```code\n{code}\n```"
                    "\nIMPORTANT: Return ONLY a JSON array. If no issues, return []."
                ),
            }
        ],
        reasoning={"effort": "medium"},
        max_output_tokens=1000,
    )

    raw_text = (response.output_text or "").strip()
    print(f"\nRAW MODEL OUTPUT for {file_path}:\n{raw_text}\n")

    if raw_text == "" or raw_text == "[]":
        return []

    start = raw_text.find("[")
    end = raw_text.rfind("]")
    candidate = raw_text[start : end + 1] if start != -1 and end != -1 else raw_text

    try:
        findings = json.loads(candidate)
        if isinstance(findings, dict):
            findings = [findings]
        if not isinstance(findings, list):
            return []
    except json.JSONDecodeError:
        print(f"WARNING: Invalid JSON for {file_path}, ignoring.")
        return []

    for f in findings:
        f.setdefault("source_file", str(file_path))

    return findings


# --------------------- file OR folder ---------------------
def analyze_path(path: Path) -> List[Dict[str, Any]]:
    if path.is_file():
        print(f"Analyzing single file: {path}")
        return analyze_file(path)

    if not path.is_dir():
        raise FileNotFoundError(f"Path not found: {path}")

    print(f"Analyzing folder recursively: {path}")
    all_findings: List[Dict[str, Any]] = []

    for file in path.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix.lower() not in INCLUDE_EXTENSIONS:
            continue
        print(f"\n--- Analyzing {file} ---")
        try:
            file_findings = analyze_file(file)
            all_findings.extend(file_findings)
        except Exception as e:
            print(f"ERROR analyzing {file}: {e}")

    return all_findings


# -------------------------- CLI ---------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="GenAI Security Code Review (file or folder)"
    )
    parser.add_argument(
        "target",
        help="File or folder path to analyze (e.g. app.py or 'File Scanner' or Src)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Optional JSON output path for findings (e.g. findings.json)",
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Also generate an HTML report (security_report.html by default).",
    )
    parser.add_argument(
        "--html-path",
        help="Custom path for HTML report (default: security_report.html)",
    )

    args = parser.parse_args()
    target_path = Path(args.target).resolve()

    results = analyze_path(target_path)

    print("\nFINAL FINDINGS:\n")
    print(json.dumps(results, indent=2, ensure_ascii=False))

    # JSON file
    if args.output:
        out_path = Path(args.output).resolve()
        out_path.write_text(
            json.dumps(results, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"\nSaved findings JSON to {out_path}")

    # HTML report
    if args.html:
        html_path = (
            Path(args.html_path).resolve()
            if args.html_path
            else Path("security_report.html").resolve()
        )
        save_html_report(results, html_path)
        print(f"Saved HTML report to {html_path}")
