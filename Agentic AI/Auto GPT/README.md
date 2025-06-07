# 🧠 Auto-GPT Deployment on AWS EC2 (v0.5.0)

This repository documents the successful deployment and testing of **Auto-GPT** (v0.5.0) on an **Ubuntu EC2 instance**, configured for research-based agentic tasks such as AI governance tool comparisons.

---

## ✅ Project Summary

We deployed Auto-GPT in a virtual environment on an EC2 instance and executed a use-case focused on **AI governance tool comparison** involving:

- **AI Verify**
- **Credo AI**
- **Z-Inspection**

Auto-GPT was configured to reason through steps, attempt web search, read documentation, and adaptively fallback when encountering API or environment constraints.

---

## ⚙️ Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Significant-Gravitas/Auto-GPT.git
cd Auto-GPT
```

### 2. Setup Python Virtual Environment

```bash
sudo apt update
sudo apt install python3.10 python3.10-venv
python3.10 -m venv venv
source venv/bin/activate
```

### 3. Install Poetry and Dependencies

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/home/ubuntu/.local/bin:$PATH"
cd classic
poetry install
```

### 4. Configure `.env`

```bash
cd original_autogpt
cp .env.template .env
nano .env
# Add your OpenAI API key:
OPENAI_API_KEY=sk-...
```

---

## 🚀 Running Auto-GPT

```bash
poetry run python -m autogpt
```

Auto-GPT will prompt for telemetry and then ask for your task description.

---

## 🧪 Use Case Tested

**Prompt:**
> Compare and summarize the top 5 open-source AI governance tools like AI Verify, Credo AI, and Z-Inspection. Output key features and differences in bullet points.

**What Happened:**
- Auto-GPT defined its internal role and strategy.
- Attempted to search using `web_search` → encountered `DuckDuckGo 202 RateLimit`.
- Attempted to `read_webpage` → failed due to missing Chrome binary.
- Fell back to asking the user for direct links or documents.

**Learning Outcome:**
Auto-GPT demonstrates adaptive agentic behavior, handling:
- Rate-limit errors
- Missing system dependencies
- User fallback requests

---

## 🔧 Next Steps

- [ ] Integrate **Google Programmable Search API** for better web search.
- [ ] Enable **Docker** and **EXECUTE_LOCAL_COMMANDS=True** for full command capabilities.
- [ ] Install Chromium for full webpage interaction:
  ```bash
  sudo apt install -y chromium-browser
  ```

---

## 🧠 Observations

| Feature                     | Status       |
|----------------------------|--------------|
| OpenAI API Integration     | ✅ Working    |
| Agent Reasoning Loop       | ✅ Active     |
| Web Search                 | ⚠️ Rate-limited |
| Web Scraping               | ❌ Chrome missing |
| Task Adaptability          | ✅ Fallback to user |
| Docker-based Code Execution| ❌ Disabled by default |

---

## 📁 Workspace

Auto-GPT saves its generated files and research inside:

```bash
Auto-GPT/classic/original_autogpt/data/agents/AutoGPT-*/workspace
```

---

## 📌 Author

Deployment managed by **[Your Name / GitHub Handle]**, using EC2 and OpenAI for experimentation with self-directed AI agents.