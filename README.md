# 🪞 DevMirror: Your AI Cognitive Code Companion

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-FF4B4B.svg)
![Gemini](https://img.shields.io/badge/AI-Google_Gemini-orange.svg)

**DevMirror** is a real-time, AI-powered developer analytics pipeline. It doesn't just look at *what* code you write; it analyzes *how* you write it. By combining AST parsing, behavioral pattern detection, and Google's Gemini AI, DevMirror acts as a real-time mirror reflecting your code complexity, cognitive thinking style, and potential anti-patterns as you type.

---

## 🚀 The Architecture (The "Exodia" Pipeline)

We built DevMirror using a highly modular microservice architecture. Six distinct components talk to each other in real-time to provide instantaneous feedback:

1. **The Bridge (VS Code Extension):** Silently runs in the background. Every time the developer presses `Ctrl+S`, it captures a snapshot of the code and pushes it to the backend.
2. **The Orchestrator (`main.py`):** A FastAPI backend that acts as the central nervous system, receiving VS Code payloads, routing them to the specialized engines, and managing the SQLite database.
3. **The Code Engine:** Uses Python `ast` and `radon` to parse code structure, calculate true Cyclomatic Complexity, and flag anti-patterns (like deep nesting or bare `except` blocks).
4. **The Pattern Engine:** Analyzes developer behavior to generate a **Cognitive Profile** (e.g., determining if the coder is a "Planner" or a "Linear Thinker").
5. **The AI Brain (Gemini):** Takes the raw metrics from the Code and Pattern engines and generates natural language refactoring advice.
6. **The Dashboard (Streamlit):** A live, auto-updating UI that visualizes the developer's metrics and AI insights in real-time.

---

## 🛠️ Tech Stack

* **Backend:** FastAPI, SQLAlchemy, SQLite, Uvicorn
* **Frontend:** Streamlit
* **Code Analysis:** Python `ast`, `radon`
* **AI Engine:** Google Gemini Pro API
* **IDE Integration:** VS Code Extension API (TypeScript/Node.js)

---

## ⚙️ Installation & Setup

Want to run DevMirror on your own machine? Follow these simple steps.

### 1. Clone the Repository
```bash
"git clone https://github.com/Mohit25f101/Dev-Mirror.git
cd Dev-Mirror
2. Set Up the Python Environment
We recommend using a virtual environment.

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
3. Install Dependencies
Install the required libraries for the backend, AI, and code engines:

Bash
pip install fastapi uvicorn sqlalchemy requests streamlit radon google-generativeai
4. Configure the AI Brain
You need a Google Gemini API key to run the AI insights.

Create a .env file in the root directory.

Add your key: GEMINI_API_KEY=your_api_key_here

🏃‍♂️ How to Run the Project
DevMirror requires three lightweight services to run simultaneously, plus the VS Code extension. Open three separate terminal windows in the root project folder.

Terminal 1: Start the Master Backend (Orchestrator)
This starts the main FastAPI server that handles the database and AI routing.

Bash
uvicorn main:app --reload --port 8000
Terminal 2: Start the Pattern Engine
This starts the behavioral analysis microservice.

Bash
cd pattern_engine
uvicorn main:app --reload --port 8003
Terminal 3: Start the Live UI Dashboard
This launches the Streamlit frontend. It will automatically open in your web browser.

Bash
streamlit run Frontend/dashboard.py
Terminal 4: Launch the VS Code Extension
Open the vscode-extension folder in a new VS Code window.

Press F5 on your keyboard (or click Run > Start Debugging).

A new "Extension Development Host" window will pop up.

In this new window, open any Python file (e.g., test.py), write some code, and press Save (Ctrl+S).

Watch the Streamlit Dashboard instantly light up with your code metrics and AI insights!

👥 The Team
Built with ❤️ during the Hackathon by:

Mohit - Backend Architecture & AI Orchestration

Gagan - UI Dashboard & VS Code Extension Bridge

Dhruv - AST Code Analysis Engine

Rohan - Behavioral Pattern Engine


### 🏆 You are done!
Paste that in, and your DevMirror project is 100% complete
