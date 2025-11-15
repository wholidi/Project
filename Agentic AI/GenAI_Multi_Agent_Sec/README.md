# 🔐 GenAI Multi-Agent Security Code Scanner

A lightweight, production-ready **multi-agent AI security reviewer** built with **FastAPI**, **Uvicorn**, and **OpenAI/Seagate GenAI models**.  
It analyzes source code, classifies vulnerabilities, and generates an executive summary — all through a multi-agent workflow.

This project upgrades the original single-agent code scanner into a **true multi-agent pipeline**:

```
ScanAgent → RiskClassifierAgent → SummaryAgent
```

Perfect for AppSec reviews, DevSecOps pipelines, internal audits, and AI-powered compliance tooling.

---

## 🌟 Features

### 🧠 Multi-Agent Architecture
- **ScanAgent** — LLM-powered static security scanner  
- **RiskClassifierAgent** — Normalizes severity + OWASP mapping  
- **SummaryAgent** — Generates security architect–level summaries  
- **Coordinator** — Orchestrates all agents into a clean workflow  

### 🔍 Codebase Scanning
- Upload **single files** or an entire **ZIP** project  
- Recursively scans `.py`, `.js`, `.ts`, `.go`, `.java`, `.cs`  
- Strict AppSec reasoning enforced by a structured LLM prompt  

### 📤 Output Includes
- Executive summary  
- Structured findings  
- OWASP category mapping  
- Multi-agent `workflow_trace`  
- Optional HTML report (single-agent mode)

---

## 📁 Project Structure

```
Sea_genai_sec_multiagent_auto_ui/
│
├── api_server.py              # FastAPI endpoints (multi-agent + single-agent)
├── ai_agent.py                # Base single-agent security analyzer
├── multi_agent_workflow.py    # NEW: Multi-agent orchestration
├── report_html.py             # HTML generator for single-agent mode
├── start_multiagent.ps1       # Start server script
├── stop_multiagent.ps1        # Stop server script
├── .env                       # API key for OpenAI/Seagate model
└── Src/                       # Sample code (optional)
```

---

## 🚀 Getting Started

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If no requirements file, install manually:

```bash
pip install fastapi uvicorn python-dotenv openai
```

---

### 2️⃣ Configure API Key

Create (or edit) `.env` inside the project folder:

```
OPENAI_API_KEY=your_key_here
```

This key is used inside `ai_agent.py` via `dotenv`.

---

### 3️⃣ Start the Multi-Agent Server

```powershell
cd C:\Sea_genai_sec_multiagent_auto_ui
.\.venv\Scripts\activate
uvicorn api_server:app --host 0.0.0.0 --port 8002 --reload
```

Or simply double-click:

```
start_multiagent.ps1
```

Swagger UI will be available at:

```
http://localhost:8002/docs
```

---

## 🧠 Multi-Agent Workflow Details

The multi-agent logic is found in:

```
multi_agent_workflow.py
```

### 🔹 **1. ScanAgent**
Runs the LLM code review using `analyze_path()`.

### 🔹 **2. RiskClassifierAgent**
Adds professional triage and OWASP mapping.

### 🔹 **3. SummaryAgent**
Produces a human-readable executive summary.

---

## 📡 API Endpoints

### 🔵 Health Check
```
GET /health
```

### 🟢 Single File Scan (single-agent)
```
POST /analyze-file
```

### 🟢 ZIP Scan → HTML (single-agent)
```
POST /analyze-zip-html
```

### 🟣 Multi-Agent File Scan (NEW)
```
POST /multi-agent-file
```

### 🟣 Multi-Agent ZIP Scan (NEW)
```
POST /multi-agent-zip
```

---

## 🛑 Stop the Server

Use:

```
stop_multiagent.ps1
```

Or manually:

```powershell
taskkill /IM uvicorn.exe /F
```

---

## 📅 Roadmap

- [ ] SecretScannerAgent  
- [ ] DependencyScannerAgent  
- [ ] Memory / audit log  
- [ ] Multi-agent UI  
- [ ] PDF report export  
- [ ] Compliance mapping (NIST/ISO/EU AI Act)

---

## ✨ Author

Created by **MLP** with assistance from ChatGPT.
