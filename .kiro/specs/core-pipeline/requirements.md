# Requirements: Real-Time Developer Analytics Pipeline

## 1. Overview

DevMirror is a real-time developer analytics platform that captures coding behavior, analyzes code quality, profiles cognitive patterns, and generates personalized AI-driven insights. The system integrates six core components into a unified end-to-end pipeline for the hackathon MVP.

## 2. User Stories

### 2.1 As a Developer
- I want my code changes to be automatically captured when I save files in VS Code
- I want to see real-time metrics about my code complexity and quality
- I want to understand my cognitive patterns and thinking style while coding
- I want personalized AI feedback that helps me improve my coding workflow
- I want to visualize my coding session history and trends over time

### 2.2 As a Team Lead
- I want to understand how my team members approach problem-solving
- I want to identify when developers are stuck in debug loops
- I want to see code quality metrics across different sessions
- I want data-driven insights to provide better mentorship

## 3. Functional Requirements

### 3.1 VS Code Extension Bridge
**Priority:** Critical

**Acceptance Criteria:**
- 3.1.1 The extension MUST activate when VS Code starts
- 3.1.2 The extension MUST track file switches and log the active file name
- 3.1.3 The extension MUST capture edit events with timestamps
- 3.1.4 The extension MUST detect save events and capture the file path
- 3.1.5 The extension MUST calculate time spent per file
- 3.1.6 The extension MUST detect edit bursts (rapid edits within 3 seconds)
- 3.1.7 The extension MUST provide a summary command to view session statistics
- 3.1.8 The extension MUST send code snapshots to the backend API on save events

### 3.2 FastAPI Orchestrator
**Priority:** Critical

**Acceptance Criteria:**
- 3.2.1 The orchestrator MUST expose a `/analyze` endpoint that accepts user_id, logs, and code_snapshot
- 3.2.2 The orchestrator MUST route code snapshots to the Code Engine for analysis
- 3.2.3 The orchestrator MUST route activity logs to the Pattern Engine for cognitive profiling
- 3.2.4 The orchestrator MUST call the Gemini AI Engine with combined metrics
- 3.2.5 The orchestrator MUST handle service failures gracefully with fallback responses
- 3.2.6 The orchestrator MUST save all analysis results to the SQLite database
- 3.2.7 The orchestrator MUST return a unified response containing code metrics, cognitive profile, and AI reflection
- 3.2.8 The orchestrator MUST support CORS for frontend communication
- 3.2.9 The orchestrator MUST log all requests and service calls for debugging

### 3.3 Code Engine (AST Analysis)
**Priority:** Critical

**Acceptance Criteria:**
- 3.3.1 The engine MUST parse Python code using AST (Abstract Syntax Tree)
- 3.3.2 The engine MUST calculate cyclomatic complexity using the Radon library
- 3.3.3 The engine MUST count the number of functions in the code
- 3.3.4 The engine MUST calculate average function length in lines
- 3.3.5 The engine MUST detect maximum nesting depth
- 3.3.6 The engine MUST detect anti-patterns including:
  - Deep nesting (depth >= 3)
  - Large functions (avg length > 30 lines)
  - High complexity (cyclomatic complexity > 10)
  - Missing modularization (no functions detected)
- 3.3.7 The engine MUST classify cognitive profiles based on code structure:
  - Over-structurer (depth >= 3 and complexity > 10)
  - Monolithic builder (avg length > 40)
  - Micro-modular thinker (func_count > 5 and avg length < 15)
  - Linear thinker (complexity < 5 and depth <= 1)
- 3.3.8 The engine MUST handle syntax errors gracefully and return error messages

### 3.4 Pattern Engine (Cognitive Profiling)
**Priority:** Critical

**Acceptance Criteria:**
- 3.4.1 The engine MUST accept activity logs with file, event, error_type, and timestamp
- 3.4.2 The engine MUST extract behavioral features including:
  - Error repeat rate
  - Average edit interval (hesitation metric)
  - Edit burstiness (rapid edits < 3 seconds apart)
  - Run/edit ratio
- 3.4.3 The engine MUST classify thinking styles:
  - Trial and Error (edit_burstiness > 3)
  - Analytical (avg_edit_interval > 25 seconds)
  - Planner (run_edit_ratio < 0.4)
  - Brute Force (error_repeat_rate > 0.3)
  - Balanced (default)
- 3.4.4 The engine MUST detect debug loops by analyzing error patterns
- 3.4.5 The engine MUST calculate a confidence score (1 - error_repeat_rate)
- 3.4.6 The engine MUST expose a `/analyze_behavior` endpoint
- 3.4.7 The engine MUST return thinking_style, weak_area, debug_loop status, and confidence

### 3.5 Gemini AI Engine
**Priority:** Critical

**Acceptance Criteria:**
- 3.5.1 The engine MUST integrate with Google Gemini API
- 3.5.2 The engine MUST auto-detect the best available Gemini model
- 3.5.3 The engine MUST generate personalized reflections based on:
  - Code snapshot
  - Thinking style
  - Cyclomatic complexity
  - Detected anti-patterns
- 3.5.4 The engine MUST produce 2-sentence reflections:
  - Sentence 1: Mirror the developer's mental state
  - Sentence 2: Provide one specific coding tip
- 3.5.5 The engine MUST handle API errors gracefully with fallback messages
- 3.5.6 The engine MUST return reflections within 5 seconds

### 3.6 Streamlit Dashboard
**Priority:** Critical

**Acceptance Criteria:**
- 3.6.1 The dashboard MUST display the AI reflection prominently as a chat message
- 3.6.2 The dashboard MUST show cognitive profile metrics:
  - Thinking style
  - Confidence level (progress bar)
  - Debug loop status (warning/success indicator)
- 3.6.3 The dashboard MUST show code complexity metrics:
  - Cyclomatic complexity score
  - List of detected anti-patterns
- 3.6.4 The dashboard MUST provide demo scenarios for testing:
  - Scenario A: Frustrated Debugger
  - Scenario B: Clean Refactoring
- 3.6.5 The dashboard MUST display session history as a line chart
- 3.6.6 The dashboard MUST use a dark theme with hacker-style aesthetics
- 3.6.7 The dashboard MUST show connection status to the backend
- 3.6.8 The dashboard MUST handle backend connection failures gracefully

## 4. Non-Functional Requirements

### 4.1 Performance
- 4.1.1 The end-to-end pipeline MUST process analysis requests within 10 seconds
- 4.1.2 The Code Engine MUST analyze code within 2 seconds
- 4.1.3 The Pattern Engine MUST process logs within 2 seconds
- 4.1.4 The dashboard MUST render updates within 1 second of receiving data

### 4.2 Reliability
- 4.2.1 The orchestrator MUST handle individual service failures without crashing
- 4.2.2 The system MUST provide fallback responses when services are unavailable
- 4.2.3 The database MUST persist all analysis results for historical tracking

### 4.3 Usability
- 4.3.1 The dashboard MUST be intuitive and require no training
- 4.3.2 The VS Code extension MUST operate transparently without disrupting workflow
- 4.3.3 Error messages MUST be clear and actionable

### 4.4 Maintainability
- 4.4.1 Each component MUST be independently deployable
- 4.4.2 The system MUST use structured logging for debugging
- 4.4.3 The codebase MUST follow Python PEP 8 style guidelines

### 4.5 Security
- 4.5.1 API keys MUST be configurable via environment variables
- 4.5.2 The system MUST NOT expose sensitive data in logs
- 4.5.3 CORS MUST be properly configured to prevent unauthorized access

## 5. Technical Constraints

### 5.1 Technology Stack
- Backend: Python 3.8+, FastAPI, SQLAlchemy
- Code Analysis: AST, Radon
- Pattern Analysis: Pandas, NumPy
- AI: Google Gemini API
- Frontend: Streamlit
- Extension: TypeScript, VS Code Extension API
- Database: SQLite

### 5.2 Integration Points
- VS Code Extension → FastAPI Orchestrator (HTTP POST)
- FastAPI Orchestrator → Code Engine (Function Call)
- FastAPI Orchestrator → Pattern Engine (HTTP POST)
- FastAPI Orchestrator → Gemini AI (API Call)
- Streamlit Dashboard → FastAPI Orchestrator (HTTP POST)

### 5.3 Data Flow
1. Developer saves code in VS Code
2. Extension captures code snapshot and activity logs
3. Extension sends data to FastAPI orchestrator
4. Orchestrator routes to Code Engine and Pattern Engine
5. Orchestrator combines results and calls Gemini AI
6. Orchestrator saves to database and returns unified response
7. Dashboard displays results in real-time

## 6. Out of Scope (Future Enhancements)

- Multi-language support (currently Python-only)
- Real-time WebSocket streaming
- Team collaboration features
- Historical trend analysis beyond session view
- Integration with GitHub/GitLab
- Custom AI model training
- Mobile dashboard
- Browser-based IDE integration

## 7. Success Metrics

- 7.1 The system successfully processes 100% of valid analysis requests
- 7.2 The AI generates contextually relevant reflections in 95% of cases
- 7.3 The dashboard loads and displays results within 2 seconds
- 7.4 The VS Code extension operates without performance degradation
- 7.5 The system handles service failures gracefully with 0% crashes
