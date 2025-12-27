# AI-Powered Cloud Cost Optimizer

An AI-driven CLI tool that analyzes cloud project descriptions, simulates cloud billing,
and generates cost optimization recommendations using Large Language Models (LLMs).

This project is designed for early-stage cloud cost planning, FinOps learning,
and architectural cost analysis.

---

## 🚀 Features

- Natural language project description input
- AI-based project profile extraction
- Synthetic cloud billing generation (6–15 records)
- Cost analysis with budget comparison
- Optimization recommendations with:
  - Estimated savings
  - Risks
  - Open-source alternatives
  - Multi-cloud options
- Rich CLI-based user interface

---

## 🏗️ Architecture Overview

User (CLI)

↓

Project Description (Text)

↓

LLM → Project Profile (JSON)

↓

LLM → Synthetic Billing Data

↓

Local Cost Aggregation

↓

LLM → Optimization Report


---

## 📁 Project Structure
### Project Directory Structure

- **cloud-cost-optimizer/**
  - **src/**
    - `core_logic.py` — Core business logic
    - `llm_client.py` — LLM interaction & validation
  - `main.py` — CLI entry point
  - `project_description.txt` — User-provided project description
  - `project_profile.json` — Extracted project profile
  - `mock_billing.json` — Synthetic billing data
  - `cost_optimization_report.json` — Final optimization report
  - `requirements.txt` — Python dependencies
  - `.env.example` — Environment variable template
  - `README.md` — Project documentation




---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/namanjain2302/cloud-cost-optimizer
cd cloud-cost-optimizer
```

2️⃣ Create virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
4️⃣ Configure environment variables

Create a .env file using the example:
```bash

cp .env.example .env
```
Add your Hugging Face API key inside .env.

▶️ How to Run

```bash
python main.py
```

--- 

## CLI Options

- Enter new project description
- Run complete cost analysis
- View recommendations
- Export report
- Exit

## 📄 Sample Artifacts Included

- project_description.txt
- project_profile.json
- mock_billing.json
- cost_optimization_report.json
  
These demonstrate a full successful run of the system.

---


## 🤖 AI Usage & Academic Integrity

AI tools were used in this project **strictly as learning and productivity aids**, and **not as substitutes for independent understanding, design decisions, or authorship**. All core logic, implementation choices, and final code were written, reviewed, and fully understood by the author.

### Tools Used

- **ChatGPT (OpenAI)**  
  Used for:
  - Clarifying system design approaches for LLM-based pipelines  
  - Debugging JSON parsing, API integration, and error-handling scenarios  
  - Refining validation logic, CLI flow, and overall code structure  

- **Perplexity AI**  
  Used for:
  - Verifying best practices related to Hugging Face Inference APIs  
  - Cross-checking model compatibility, request formats, and response constraints  

All AI-assisted suggestions were **selectively applied, adapted, and validated** to ensure correctness, originality, and compliance with academic integrity guidelines.

---


### 🧰 Technologies Used


- Hugging Face Inference API (LLM-based JSON extraction and analysis)
- Open-source LLMs (Qwen series)
- Python (Rich, dotenv)

---

## 🎥 Demo Video

🔗 [View Demo Video](https://drive.google.com/file/d/1-w8JHGAf4u0-Id6kpFQLzBmMGpSig3RB/view?usp=sharing)

---

### ⚠️ Disclaimer

This tool generates synthetic billing data for educational and planning purposes.
It is not connected to real cloud billing APIs.

