# Design: Real-Time Developer Analytics Pipeline

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         VS Code IDE                              │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         DevMirror Extension (TypeScript)                │    │
│  │  - File tracking                                        │    │
│  │  - Edit event capture                                   │    │
│  │  - Time tracking                                        │    │
│  └────────────────────┬───────────────────────────────────┘    │
└────────────────────────┼────────────────────────────────────────┘
                         │ HTTP POST
                         │ {user_id, logs[], code_snapshot}
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              FastAPI Orchestrator (main.py)                      │
│                     Port 8000                                    │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  /analyze endpoint                                    │      │
│  │  - Request validation                                 │      │
│  │  - Service coordination                               │      │
│  │  - Response aggregation                               │      │
│  │  - Database persistence                               │      │
│  └──┬────────────────┬────────────────┬──────────────┬──┘      │
└─────┼────────────────┼────────────────┼──────────────┼─────────┘
      │                │                │              │
      │ Function Call  │ HTTP POST      │ API Call     │ SQLAlchemy
      ▼                ▼                ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Code Engine  │ │Pattern Engine│ │ Gemini AI    │ │   SQLite     │
│ (analyzer/)  │ │(pattern_eng/)│ │ (ai_engine)  │ │ (devmirror   │
│              │ │              │ │              │ │  .db)        │
│ Port: N/A    │ │ Port: 8003   │ │ External API │ │              │
│ (In-process) │ │              │ │              │ │              │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────────────┘
       │                │                │
       │ Returns        │ Returns        │ Returns
       │ code_metrics   │ cognitive_     │ ai_reflection
       │                │ profile        │
       └────────────────┴────────────────┘
                         │
                         │ Unified Response
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│           Streamlit Dashboard (Frontend/dashboard.py)           │
│                     Port 8501                                    │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  - AI Reflection Display                             │      │
│  │  - Cognitive Profile Metrics                         │      │
│  │  - Code Complexity Visualization                     │      │
│  │  - Session History Charts                            │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Responsibilities

#### 1.2.1 VS Code Extension Bridge
- **Purpose:** Capture developer activity in real-time
- **Technology:** TypeScript, VS Code Extension API
- **Key Functions:**
  - Track active file switches
  - Monitor edit events with timestamps
  - Detect save operations
  - Calculate time spent per file
  - Identify edit bursts (rapid changes)
  - Send data to orchestrator

#### 1.2.2 FastAPI Orchestrator
- **Purpose:** Central hub for request routing and coordination
- **Technology:** FastAPI, Python 3.8+
- **Key Functions:**
  - Validate incoming requests
  - Route code to Code Engine
  - Route logs to Pattern Engine
  - Aggregate results from all engines
  - Call Gemini AI with combined context
  - Persist results to database
  - Handle service failures gracefully

#### 1.2.3 Code Engine (Dhruv's Engine)
- **Purpose:** Analyze code structure and complexity
- **Technology:** Python AST, Radon
- **Key Functions:**
  - Parse Python code into AST
  - Calculate cyclomatic complexity
  - Count functions and measure lengths
  - Detect nesting depth
  - Identify anti-patterns
  - Classify code-based cognitive profiles

#### 1.2.4 Pattern Engine (Rohan's Engine)
- **Purpose:** Profile developer cognitive patterns
- **Technology:** Python, Pandas
- **Key Functions:**
  - Extract behavioral features from logs
  - Calculate error repeat rate
  - Measure edit intervals (hesitation)
  - Detect edit burstiness
  - Classify thinking styles
  - Identify debug loops

#### 1.2.5 Gemini AI Engine
- **Purpose:** Generate personalized insights
- **Technology:** Google Gemini API
- **Key Functions:**
  - Auto-detect best available model
  - Synthesize code + cognitive data
  - Generate 2-sentence reflections
  - Mirror developer mental state
  - Provide actionable coding tips

#### 1.2.6 Streamlit Dashboard
- **Purpose:** Visualize analytics in real-time
- **Technology:** Streamlit, Python
- **Key Functions:**
  - Display AI reflections
  - Show cognitive profile metrics
  - Visualize code complexity
  - Render session history
  - Provide demo scenarios

## 2. Data Models

### 2.1 Request Schema (Input to Orchestrator)

```python
class ActivityLog(BaseModel):
    file: str                    # e.g., "api.py"
    event: str                   # "edit", "save", "run", "error"
    error_type: Optional[str]    # "SyntaxError", "TypeError", etc.
    timestamp: str               # ISO 8601 format

class AnalysisRequest(BaseModel):
    user_id: str                 # Unique developer identifier
    logs: List[ActivityLog]      # Activity history
    code_snapshot: Optional[str] # Current code content
```

### 2.2 Response Schema (Output from Orchestrator)

```python
class AnalysisResponse(BaseModel):
    status: str                  # "success" or "error"
    code_analysis: dict          # From Code Engine
    cognitive_profile: dict      # From Pattern Engine
    ai_reflection: str           # From Gemini AI
    saved_at: datetime           # Database timestamp
```

### 2.3 Code Analysis Output

```python
{
    "function_count": int,
    "avg_function_length": float,
    "max_nesting_depth": int,
    "cyclomatic_complexity": float,
    "insights": List[str],           # Anti-pattern warnings
    "cognitive_profile": List[str]   # Code-based classifications
}
```

### 2.4 Cognitive Profile Output

```python
{
    "thinking_style": str,      # "trial_and_error", "analytical", etc.
    "weak_area": str,           # "debugging", "general"
    "debug_loop": bool,         # True if stuck
    "confidence": float         # 0.0 to 1.0
}
```

### 2.5 Database Schema

```python
class AnalysisResult(Base):
    __tablename__ = "analysis_history"
    
    id: int                     # Primary key
    user_id: str                # Developer identifier
    timestamp: datetime         # Analysis time
    code_metrics: JSON          # Code Engine results
    cognitive_profile: JSON     # Pattern Engine results
    ai_reflection: str          # Gemini AI output
```

## 3. Component Design Details

### 3.1 VS Code Extension

#### 3.1.1 State Management
```typescript
let currentFile: string | null = null;
let fileStartTime: number | null = null;
const timeSpent: Record<string, number> = {};
let lastEditTime: number | null = null;
let editCount = 0;
```

#### 3.1.2 Event Handlers
- **onDidChangeActiveTextEditor:** Track file switches and calculate time spent
- **onDidChangeTextDocument:** Detect edits and measure burstiness
- **onDidSaveTextDocument:** Capture save events and trigger backend call

#### 3.1.3 Backend Communication
```typescript
// POST to http://127.0.0.1:8000/analyze
{
    user_id: "developer_id",
    code_snapshot: documentContent,
    logs: activityLogArray
}
```

### 3.2 FastAPI Orchestrator

#### 3.2.1 Request Flow
1. Receive POST request at `/analyze`
2. Validate request schema
3. Call Code Engine (in-process function)
4. Call Pattern Engine (HTTP POST to port 8003)
5. Map and normalize results
6. Call Gemini AI with combined context
7. Save to database
8. Return unified response

#### 3.2.2 Error Handling Strategy
```python
def safe_post_request(url: str, payload: dict, default_response: dict):
    try:
        response = requests.post(url, json=payload, timeout=2)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.warning(f"Service Down ({url}): {e}")
    
    return default_response  # Graceful degradation
```

#### 3.2.3 Data Mapping
The orchestrator normalizes field names to ensure consistency:
```python
# Map Code Engine output
actual_complexity = code_result.get("cyclomatic_complexity", 0)
code_result["complexity"] = actual_complexity
code_result["bad_patterns"] = code_result.get("insights", [])
```

### 3.3 Code Engine

#### 3.3.1 AST Analysis Pipeline
```python
def analyze_code(code: str) -> dict:
    # Step 1: Parse AST
    ast_metrics = parse_code(code)
    
    # Step 2: Calculate complexity
    complexity_metrics = calculate_complexity(code)
    
    # Step 3: Detect patterns
    pattern_data = detect_patterns(combined_metrics)
    
    return combined_metrics
```

#### 3.3.2 Complexity Calculation
Uses Radon library to calculate cyclomatic complexity:
```python
from radon.complexity import cc_visit

results = cc_visit(code)
avg_complexity = sum(block.complexity for block in results) / len(results)
```

#### 3.3.3 Pattern Detection Rules
```python
if depth >= 3:
    insights.append("Deep nesting detected")
if avg_len > 30:
    insights.append("Large function size detected")
if complexity > 10:
    insights.append("High cyclomatic complexity")
```

### 3.4 Pattern Engine

#### 3.4.1 Feature Extraction
```python
def extract_features(logs):
    df = pd.DataFrame(logs)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Calculate behavioral metrics
    error_repeat_rate = len(error_events) / total_events
    avg_edit_interval = edit_times.mean()
    edit_burstiness = (edit_times < 3).sum()
    run_edit_ratio = len(run_events) / len(edit_events)
    
    return features
```

#### 3.4.2 Thinking Style Classification
```python
def classify_thinking_style(features):
    if features["edit_burstiness"] > 3:
        return "trial_and_error"
    if features["avg_edit_interval"] > 25:
        return "analytical"
    if features["run_edit_ratio"] < 0.4:
        return "planner"
    if features["error_repeat_rate"] > 0.3:
        return "brute_force"
    return "balanced"
```

#### 3.4.3 Debug Loop Detection
Analyzes error patterns to identify when developers are stuck:
```python
def detect_debug_loop(logs):
    # Check for repeated errors in short time window
    # Return True if stuck pattern detected
```

### 3.5 Gemini AI Engine

#### 3.5.1 Model Selection
```python
available_models = [
    m.name for m in genai.list_models() 
    if 'generateContent' in m.supported_generation_methods
]
model_name = available_models[0]  # Auto-select best model
```

#### 3.5.2 Prompt Engineering
```python
prompt = f"""
You are DevMirror, an expert AI coding mentor.
Thinking Style: "{thinking_style}"
Code Complexity: {complexity}
Anti-patterns: {errors}

CODE:
{code_snapshot}

TASK:
Give a 2-sentence reflection.
1. Mirror their mental state.
2. Give one specific coding tip for that code.
"""
```

#### 3.5.3 Response Generation
```python
response = model.generate_content(prompt)
return response.text.strip()
```

### 3.6 Streamlit Dashboard

#### 3.6.1 Layout Structure
```python
# Header with logo and title
# Sidebar with connection status and demo scenarios
# Main area with:
#   - AI Reflection (chat message)
#   - Metrics Grid (2 columns)
#     - Left: Cognitive Profile
#     - Right: Code Complexity
#   - Session History (line chart)
```

#### 3.6.2 Demo Scenarios
```python
# Scenario A: Frustrated Debugger
payload = {
    "user_id": "demo_user_A",
    "code_snapshot": "def fetch_data():\n    try:\n       return requests.get(url)\n    except:\n       pass",
    "logs": [
        {"file": "api.py", "event": "error", "error_type": "SyntaxError", "timestamp": "10:01:00"},
        {"file": "api.py", "event": "edit", "timestamp": "10:01:05"},
        {"file": "api.py", "event": "error", "error_type": "SyntaxError", "timestamp": "10:01:10"}
    ]
}
```

#### 3.6.3 Visualization Components
- **AI Reflection:** Chat message with assistant avatar
- **Cognitive Profile:** Metric card with thinking style, confidence progress bar, debug loop indicator
- **Code Complexity:** Metric card with complexity score and anti-pattern list
- **Session History:** Line chart showing focus score and errors over time

## 4. Integration Patterns

### 4.1 Synchronous Integration (Code Engine)
The Code Engine is called as an in-process function for performance:
```python
from analyzer.metrics_builder import analyze_code
code_result = analyze_code(request.code_snapshot)
```

### 4.2 Asynchronous Integration (Pattern Engine)
The Pattern Engine runs as a separate FastAPI service:
```python
response = requests.post(
    "http://127.0.0.1:8003/analyze_behavior",
    json=payload,
    timeout=2
)
```

### 4.3 External API Integration (Gemini)
```python
import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name)
response = model.generate_content(prompt)
```

## 5. Error Handling and Resilience

### 5.1 Service Failure Handling
```python
# Fallback responses for each service
CODE_ENGINE_FALLBACK = {"cyclomatic_complexity": 0, "insights": []}
PATTERN_ENGINE_FALLBACK = {"thinking_style": "Unknown", "confidence": 0.0}
AI_ENGINE_FALLBACK = "DevMirror is offline (AI Error)"
```

### 5.2 Timeout Configuration
- Code Engine: No timeout (in-process)
- Pattern Engine: 2 seconds
- Gemini AI: 5 seconds (implicit)

### 5.3 Logging Strategy
```python
logger.info(f"⚡ Analysis requested for user: {request.user_id}")
logger.info(f"📡 Calling: {url}")
logger.warning(f"⚠️ Service Down ({url}): {e}")
logger.info(f"🛡️ Using FALLBACK data for {url}")
logger.info("✅ Analysis saved to DB.")
```

## 6. Deployment Architecture

### 6.1 Service Ports
- FastAPI Orchestrator: 8000
- Pattern Engine: 8003
- Streamlit Dashboard: 8501
- Code Engine: N/A (in-process)

### 6.2 Startup Sequence
1. Start FastAPI Orchestrator: `uvicorn main:app --port 8000`
2. Start Pattern Engine: `uvicorn pattern_engine.api:app --port 8003`
3. Start Streamlit Dashboard: `streamlit run Frontend/dashboard.py`
4. Install VS Code Extension: Load from `vscode-extension/`

### 6.3 Database Initialization
```python
models.Base.metadata.create_all(bind=engine)
```
SQLite database is auto-created at `./devmirror.db`

## 7. Performance Considerations

### 7.1 Optimization Strategies
- Code Engine runs in-process to avoid network overhead
- Pattern Engine uses Pandas for efficient log processing
- Database uses SQLite for simplicity (suitable for MVP)
- Dashboard caches session state to avoid redundant API calls

### 7.2 Scalability Limitations (MVP)
- SQLite is single-threaded (not suitable for production)
- No connection pooling for Pattern Engine
- No caching layer for repeated analyses
- No load balancing or horizontal scaling

## 8. Security Considerations

### 8.1 API Key Management
```python
# Current: Hardcoded (MVP only)
GEMINI_API_KEY = "AIzaSy..."

# Production: Environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

### 8.2 CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # MVP: Allow all
    # Production: Restrict to specific origins
)
```

### 8.3 Input Validation
All requests are validated using Pydantic schemas to prevent injection attacks.

## 9. Testing Strategy

### 9.1 Unit Testing
- Code Engine: Test AST parsing, complexity calculation, pattern detection
- Pattern Engine: Test feature extraction, thinking style classification
- AI Engine: Mock Gemini API responses

### 9.2 Integration Testing
- Test orchestrator with all services running
- Test orchestrator with services down (fallback behavior)
- Test end-to-end flow from extension to dashboard

### 9.3 Demo Scenarios
- Scenario A: Frustrated Debugger (high error rate, debug loop)
- Scenario B: Clean Refactoring (low complexity, analytical style)

## 10. Future Enhancements

### 10.1 Real-Time Streaming
Replace HTTP polling with WebSocket connections for live updates.

### 10.2 Multi-Language Support
Extend Code Engine to support JavaScript, TypeScript, Java, etc.

### 10.3 Advanced Analytics
- Trend analysis over weeks/months
- Team comparison dashboards
- Predictive burnout detection

### 10.4 Production Readiness
- Replace SQLite with PostgreSQL
- Add Redis caching layer
- Implement authentication and authorization
- Deploy on cloud infrastructure (AWS, GCP, Azure)

## 11. Correctness Properties

### 11.1 Code Engine Properties
**Property 1.1:** For any valid Python code, the cyclomatic complexity MUST be >= 1.
**Property 1.2:** The number of detected functions MUST equal the count of `def` statements in the AST.
**Property 1.3:** Maximum nesting depth MUST be >= 0 and <= actual nesting in code.

### 11.2 Pattern Engine Properties
**Property 2.1:** Error repeat rate MUST be in the range [0.0, 1.0].
**Property 2.2:** Confidence score MUST equal (1 - error_repeat_rate).
**Property 2.3:** Thinking style classification MUST return one of the five defined categories.

### 11.3 Orchestrator Properties
**Property 3.1:** If Code Engine fails, the orchestrator MUST return a fallback response without crashing.
**Property 3.2:** All successful analyses MUST be persisted to the database.
**Property 3.3:** Response time MUST be <= 10 seconds for 95% of requests.

### 11.4 AI Engine Properties
**Property 4.1:** AI reflections MUST contain exactly 2 sentences.
**Property 4.2:** If Gemini API fails, the engine MUST return an error message (not crash).

### 11.5 Dashboard Properties
**Property 5.1:** The dashboard MUST display all three result components (code, cognitive, AI).
**Property 5.2:** If backend is unreachable, the dashboard MUST show an error message.

## 12. Acceptance Testing

### 12.1 End-to-End Test Cases

**Test Case 1: Happy Path**
1. Developer saves code in VS Code
2. Extension sends request to orchestrator
3. All engines process successfully
4. Dashboard displays complete results
5. Database contains new record

**Test Case 2: Code Engine Failure**
1. Send invalid Python code
2. Code Engine returns error
3. Orchestrator uses fallback
4. Dashboard shows partial results

**Test Case 3: Pattern Engine Failure**
1. Pattern Engine service is down
2. Orchestrator detects timeout
3. Orchestrator uses fallback cognitive profile
4. Dashboard shows "Unknown" thinking style

**Test Case 4: AI Engine Failure**
1. Invalid Gemini API key
2. AI Engine catches exception
3. Returns error message
4. Dashboard displays error in reflection area

## 13. Documentation Requirements

### 13.1 README Files
- Root README: Project overview, setup instructions
- Extension README: Installation and usage
- Pattern Engine README: API documentation

### 13.2 Code Comments
- All complex algorithms MUST have explanatory comments
- All API endpoints MUST have docstrings
- All configuration variables MUST be documented

### 13.3 API Documentation
FastAPI auto-generates docs at `/docs` endpoint.

## 14. Hackathon Submission Checklist

- [x] All six components are integrated
- [x] End-to-end pipeline is functional
- [x] Demo scenarios work reliably
- [x] Dashboard is visually polished
- [x] Code is documented
- [x] Requirements and design docs are complete
- [ ] Video demo is recorded
- [ ] Presentation slides are prepared
- [ ] GitHub repository is public
