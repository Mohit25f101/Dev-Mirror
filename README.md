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
