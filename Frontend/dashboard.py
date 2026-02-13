import streamlit as st
import requests
import json
import time
import pandas as pd

# --- CONFIGURATION ---
# This points to YOUR backend (main.py) running on Port 8000
BACKEND_URL = "http://127.0.0.1:8000/analyze"

# --- PAGE SETUP ---
st.set_page_config(
    page_title="DevMirror AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS (Hacker / Dark Mode Style) ---
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
        background-color: #00FF94; 
        color: black;
        border: none;
    }
    .stButton>button:hover {
        background-color: #00CC76;
        color: black;
    }
    h1, h2, h3 {
        color: #00FF94;
    }
    .metric-card {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #444;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
with col2:
    st.title("DevMirror")
    st.caption("The AI that teaches you by watching you build.")

st.divider()

# --- SIDEBAR (CONTROLS) ---
with st.sidebar:
    st.header("🔌 Live Connection")
    status = st.empty()
    status.success("🟢 Connected to VS Code Extension")
    
    st.markdown("### 🛠️ Developer Simulation")
    st.info("Since we are in a demo, click a button below to simulate real-time coding events.")
    
    # SCENARIO 1: The Frustrated Debugger
    if st.button("Scenario A: Frustrated Debugger"):
        with st.spinner("Analyzing Neural Patterns..."):
            payload = {
                "user_id": "demo_user_A",
                "code_snapshot": "def fetch_data():\n    try:\n       return requests.get(url)\n    except:\n       pass # bad practice",
                "logs": [
                    {"file": "api.py", "event": "error", "error_type": "SyntaxError", "timestamp": "10:01:00"},
                    {"file": "api.py", "event": "edit", "timestamp": "10:01:05"},
                    {"file": "api.py", "event": "error", "error_type": "SyntaxError", "timestamp": "10:01:10"},
                    {"file": "api.py", "event": "save", "timestamp": "10:01:12"}
                ]
            }
            try:
                response = requests.post(BACKEND_URL, json=payload)
                if response.status_code == 200:
                    st.session_state['data'] = response.json()
                    st.toast("Analysis Complete!", icon="✅")
                else:
                    st.error(f"Backend Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")
                st.caption("Make sure 'uvicorn main:app' is running on port 8000")

    # SCENARIO 2: The Clean Coder
    if st.button("Scenario B: Clean Refactoring"):
        with st.spinner("Analyzing Neural Patterns..."):
            payload = {
                "user_id": "demo_user_B",
                "code_snapshot": "class DataHandler:\n    def __init__(self):\n        self.data = []",
                "logs": [
                    {"file": "handler.py", "event": "edit", "timestamp": "10:05:00"},
                    {"file": "handler.py", "event": "save", "timestamp": "10:05:30"}
                ]
            }
            try:
                response = requests.post(BACKEND_URL, json=payload)
                if response.status_code == 200:
                    st.session_state['data'] = response.json()
                    st.toast("Analysis Complete!", icon="✅")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

# --- MAIN DASHBOARD CONTENT ---
if 'data' in st.session_state:
    data = st.session_state['data']
    
    # 1. THE AI REFLECTION (This is the most important part)
    st.markdown("### 🔮 Cognitive Reflection")
    reflection_text = data.get("ai_reflection", "Thinking...")
    
    # Display as a chat message
    with st.chat_message("assistant", avatar="🤖"):
        st.write(f"**DevMirror Insight:**")
        st.write(reflection_text)
    
    st.divider()

    # 2. METRICS GRID
    col_a, col_b = st.columns(2)
    
    # --- LEFT COLUMN: Rohan's Data (Thinking) ---
    with col_a:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader("🧠 Cognitive Profile")
        
        profile = data.get("cognitive_profile", {})
        style = profile.get("thinking_style", "Analyzing...")
        confidence = profile.get("confidence", 0.0)
        
        st.metric("Thinking Style", style, delta="Detected Pattern")
        
        st.write("Confidence Level")
        st.progress(confidence)
        
        if profile.get("debug_loop"):
            st.error("⚠️ STUCK IN DEBUG LOOP DETECTED")
        else:
            st.success("✅ Workflow is Flowing")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- RIGHT COLUMN: Dhruv's Data (Code) ---
    with col_b:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader("🧩 Code Complexity")
        
        code = data.get("code_analysis", {})
        comp = code.get("complexity", 0)
        
        st.metric("Cyclomatic Complexity", comp)
        
        bad_patterns = code.get("bad_patterns", [])
        if bad_patterns:
            st.warning("**Anti-Patterns Found:**")
            for p in bad_patterns:
                st.write(f"❌ {p}")
        else:
            st.success("✅ Clean Code Structure")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. HISTORY TABLE (From Database)
    st.markdown("### 📜 Session History")
    # Just a placeholder for demo visualization
    history_data = pd.DataFrame({
        "Time": ["10:00", "10:05", "10:10"],
        "Focus Score": [80, 65, 40],
        "Errors": [0, 2, 5]
    })
    st.line_chart(history_data.set_index("Time"))

else:
    # EMPTY STATE
    st.info("👈 Waiting for input... Click a Scenario button in the sidebar to start the demo.")