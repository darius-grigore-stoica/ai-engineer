# ai-engineer
# 1. AI Code Reviewer

An automated code review assistant powered by **Gemini 3 Flash** and **FastAPI**. This tool listens for code changes, analyzes diffs using a "Senior Engineer" persona, and provides structured feedback on security, performance, and maintainability.

---

## 🚀 Features
* **LLM-Powered Insights:** Uses Google's Gemini model to provide context-aware reviews.
* **Persona-Driven:** Configured with a `system_instruction` parameter to act as a Principal Software Engineer.
* **FastAPI Backend:** A lightweight, high-performance webhook listener.
* **Pydantic Validation:** Ensures all AI responses follow a strict JSON schema for reliability and parsing.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Framework:** FastAPI
* **AI Model:** Gemini 3 Flash (via Google GenAI SDK)
* **Environment:** Python-dotenv for secure secret management

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/](https://github.com/)[YOUR_USERNAME]/ai_engineer.git
cd ai_engineer/ai_code_reviewer
```

### 2. Install Dependencies
Create a virtual environment and install the required packages:
```bash
# Create environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the `ai_code_reviewer/` directory.
**⚠️ CRITICAL: The .gitignore is configured to block this file. Never commit it to GitHub.**
```text
GEMINI_API_KEY=your_api_key_here
PORT=8000
```

### 4. Run the Application
Start the server using Uvicorn:
```bash
uvicorn main:app --reload
```

---

## 📖 Project Architecture

The project is structured to separate the API logic from the LLM logic:

* **`main.py`**: The entry point. Handles FastAPI routing and receives code diffs via POST requests.
* **`llm_client.py`**: The "Brain." It manages the connection to Gemini, defines the **System Prompt** (Persona), and parses the AI's response.
* **`.gitignore`**: Uses `**/.env` to ensure secrets are ignored across all subdirectories.