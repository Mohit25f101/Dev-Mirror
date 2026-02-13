from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from analyzer.metrics_builder import analyze_code
import requests
import logging
import json
import ai_engine

# --- IMPORT YOUR MODULES ---
import models
import schemas
from database import engine, get_db

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DevMirror-Hub")

# --- CREATE DATABASE TABLES ---
models.Base.metadata.create_all(bind=engine)

# --- INITIALIZE APP ---
app = FastAPI(title="DevMirror Backend Orchestrator")

# --- CORS (Allow Frontend to Talk to Us) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIG: TEAMMATE URLS ---
PATTERN_ENGINE_URL = "http://127.0.0.1:8003/analyze_behavior"
CODE_ENGINE_URL = "http://127.0.0.1:8001/analyze_code"


# --- HELPER: SAFE REQUEST ---
def safe_post_request(url: str, payload: dict, default_response: dict):
    try:
        logger.info(f"📡 Calling: {url}")
        response = requests.post(url, json=payload, timeout=2)
        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(f"⚠️ Service Error {response.status_code} from {url}")
    except Exception as e:
        logger.warning(f"⚠️ Service Down ({url}): {e}")
    
    logger.info(f"🛡️ Using FALLBACK data for {url}")
    return default_response


# --- MAIN ENDPOINT ---
@app.post("/analyze", response_model=schemas.AnalysisResponse)
def analyze_dev_mirror(request: schemas.AnalysisRequest, db: Session = Depends(get_db)):
    logger.info(f"⚡ Analysis requested for user: {request.user_id}")

    # --- 1. DHRUV'S REAL CODE ENGINE ---
    code_result = analyze_code(request.code_snapshot)
    
    # Safety Net: If Dhruv's code crashes, give it a default empty dictionary
    if not code_result:
        code_result = {}
        
    print("🚨 RAW DHRUV RESULT:", code_result)
    
    # ⚡ THE FIX: Map Dhruv's exact keys so the UI and AI can read them!
    actual_complexity = code_result.get("cyclomatic_complexity", 0)
    actual_insights = code_result.get("insights", [])
    
    # We inject both names into the dictionary to guarantee Streamlit finds it
    code_result["complexity"] = actual_complexity
    code_result["cyclomatic_complexity"] = actual_complexity
    code_result["bad_patterns"] = actual_insights
    
    # --- 2. Call Rohan (Pattern Engine) ---
    logs_data = [log.dict() for log in request.logs]
    
    rohan_payload = {
        "user_id": request.user_id,
        "session_id": "demo_session_1",  
        "logs": logs_data
    }

    pattern_result = safe_post_request(
        PATTERN_ENGINE_URL,
        rohan_payload,  
        default_response={"thinking_style": "Unknown (Fallback)", "confidence": 0.0, "debug_loop": False}
    )

    # --- 3. Generate AI Reflection (REAL AI) ---
    style = pattern_result.get("thinking_style", "Unknown")

    reflection_text = ai_engine.get_ai_reflection(
        code_snapshot=request.code_snapshot,
        thinking_style=style,
        complexity=actual_complexity, # Now passing the real mapped number!
        errors=actual_insights        # Now passing Dhruv's real insights!
    )

    # --- 4. Save to Database ---
    db_record = models.AnalysisResult(
        user_id=request.user_id,
        code_metrics=code_result,
        cognitive_profile=pattern_result,
        ai_reflection=reflection_text
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    logger.info("✅ Analysis saved to DB.")

    return {
        "status": "success",
        "code_analysis": code_result,
        "cognitive_profile": pattern_result,
        "ai_reflection": reflection_text,
        "saved_at": db_record.timestamp
    }