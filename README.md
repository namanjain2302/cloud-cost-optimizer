# ☁️ Cloud Cost Optimizer (LLM-Powered)

AI-powered **multi-cloud cost optimization tool** that analyzes project descriptions, generates realistic billing data, and provides actionable recommendations for cost savings across **AWS**, **Azure**, and **GCP**.

---

## 🧭 Overview

The Cloud Cost Optimizer helps software teams get detailed insights into cloud spending
patterns and improve architecture efficiency using Large Language Models (LLMs).  

It can:
- Understand a project description and extract metadata (budget, tech stack, etc.)
- Simulate monthly billing data based on realistic service usage
- Analyze spending and generate AI-powered cost optimization recommendations
- Export results in structured JSON reports

---
## 🏗️ Project Structure

📦 **cloud-cost-optimizer**  
┣ 📄 `main.py` — Entry point CLI  
┣ 📄 `requirements.txt` — Dependencies list    
┣ 📄 `README.md` — Documentation  
┗ 📂 **src**   
&nbsp;&nbsp;&nbsp;┣ 📄 `core_logic.py` — Handles business logic  
&nbsp;&nbsp;&nbsp;┗ 📄 `llm_client.py` — Manages LLM API communication  


## 🚀 Quick Start

Follow these steps to get up and running:

```bash
git clone https://github.com/namanjain2302/cloud-cost-optimizer
cd cloud-cost-optimizer
pip install -r requirements.txt
```
🔑 Environment Setup

Create a .env file in the project root and add your Hugging Face API key:
```bash
HF_API_KEY=your_api_key_here
```

▶️ Run the Application

```bash
python main.py
```

