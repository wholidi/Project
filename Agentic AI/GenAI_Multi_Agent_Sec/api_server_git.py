from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from multi_agent_workflow import run_multi_agent_workflow

from pathlib import Path
import tempfile
import zipfile
from typing import List, Dict, Any

from ai_agent import analyze_file, analyze_path
from report_html import findings_to_html

app = FastAPI(
    title="GenAI Security Agent",
    description="Seagate GenAI-powered security review service",
    version="1.0.0",
)

# -----------------------------------------
# Health check
# -----------------------------------------
@app.get("/health")
async def health():
    return {"status": "ok"}


# -----------------------------------------
# Analyze a single uploaded file -> JSON
# -----------------------------------------
@app.post("/analyze-file")
async def analyze_single_file(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = Path(tmp.name)

    try:
        findings: List[Dict[str, Any]] = analyze_file(tmp_path)
    finally:
        tmp_path.unlink(missing_ok=True)

    return JSONResponse(content=findings)


# -----------------------------------------
# Analyze a ZIP -> HTML report
# -----------------------------------------
@app.post("/analyze-zip-html", response_class=HTMLResponse)
async def analyze_zip_and_return_html(zip_file: UploadFile = File(...)):
    """
    Upload a ZIP containing a codebase.
    Returns a pretty HTML report.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        zip_path = tmp_dir_path / "project.zip"

        contents = await zip_file.read()
        zip_path.write_bytes(contents)

        extract_path = tmp_dir_path / "src"
        extract_path.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_path)

        findings: List[Dict[str, Any]] = analyze_path(extract_path)

    html_doc = findings_to_html(findings)
    return HTMLResponse(content=html_doc)


# -----------------------------------------
# Simple UI page -> upload ZIP & see HTML
# -----------------------------------------
@app.get("/ui", response_class=HTMLResponse)
async def upload_ui():
    html_page = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8"/>
      <title>GenAI Security Agent – UI</title>
      <style>
        body {
          font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          background: #f5f7fb;
          margin: 0;
          padding: 40px;
          display: flex;
          justify-content: center;
        }
        .card {
          background: #fff;
          padding: 24px 28px;
          max-width: 540px;
          width: 100%;
          box-shadow: 0 4px 12px rgba(0,0,0,0.08);
          border-radius: 12px;
        }
        h1 {
          margin-top: 0;
          font-size: 22px;
        }
        p {
          color: #555;
          font-size: 14px;
        }
        input[type="file"] {
          margin-top: 8px;
          margin-bottom: 16px;
        }
        button {
          background: #2563eb;
          border: none;
          color: #fff;
          padding: 8px 16px;
          border-radius: 6px;
          font-size: 14px;
          cursor: pointer;
        }
        button:hover {
          background: #1d4ed8;
        }
        .hint {
          font-size: 12px;
          color: #777;
          margin-top: 4px;
        }
      </style>
    </head>
    <body>
      <div class="card">
        <h1>GenAI Security Agent</h1>
        <p>Upload a ZIP archive of your codebase. The service will analyze it for security issues and display an HTML report.</p>

        <form method="post" action="/analyze-zip-html" enctype="multipart/form-data">
          <label for="zip_file">ZIP file:</label><br/>
          <input type="file" id="zip_file" name="zip_file" accept=".zip" required />
          <div class="hint">Example: compress your <code>Src</code> or <code>File Scanner</code> folder into a .zip file.</div>
          <br/>
          <button type="submit">Analyze &amp; View Report</button>
        </form>
      </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_page)

@app.post("/multi-agent-zip", response_class=JSONResponse)
async def multi_agent_zip(zip_file: UploadFile = File(...)):
    """
    Upload a ZIP, run the multi-agent workflow, and return JSON
    with both a summary and enriched findings.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        zip_path = tmp_dir_path / "project.zip"

        contents = await zip_file.read()
        zip_path.write_bytes(contents)

        extract_path = tmp_dir_path / "src"
        extract_path.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_path)

        result = run_multi_agent_workflow(extract_path)

    return JSONResponse(content=result)

@app.post("/multi-agent-file", response_class=JSONResponse)
async def multi_agent_single_file(file: UploadFile = File(...)):
    """
    Upload a single source file.
    The service wraps it in a temp folder and runs the multi-agent workflow:
      ScanAgent -> RiskClassifierAgent -> SummaryAgent
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)

        # Save the uploaded file into the temp folder
        tmp_file_path = tmp_dir_path / file.filename
        contents = await file.read()
        tmp_file_path.write_bytes(contents)

        # Reuse the same workflow as ZIP analysis
        result = run_multi_agent_workflow(tmp_dir_path)

    return JSONResponse(content=result)
