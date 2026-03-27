# Astronomy AI Agent

An AI-powered astronomy assistant built using Google ADK and Gemini, deployed on Cloud Run using ADK’s web interface.

----------------------------------------
OVERVIEW
----------------------------------------
This agent explains astronomy concepts in simple, beginner-friendly language.

It uses:
- Gemini for reasoning
- Wikipedia for factual data
- ADK for agent orchestration
- Cloud Run for deployment

----------------------------------------
FEATURES
----------------------------------------
- Astronomy question answering
- Simple explanations (<=150 words)
- Wikipedia-powered research
- Multi-agent workflow (Research -> Explanation)
- Serverless deployment on Cloud Run
- ADK Web UI (no FastAPI required)

----------------------------------------
ARCHITECTURE
----------------------------------------
```
User (ADK Web UI)
    ↓
Root Agent
    ↓
Tool: Save Query
    ↓
Research Agent
    ↓
Wikipedia Tool
    ↓
Explanation Agent
    ↓
Final Response
```

----------------------------------------
TECH STACK
----------------------------------------
- Python
- Google ADK
- Gemini 2.5 Flash
- LangChain + Wikipedia
- Google Cloud Run

----------------------------------------
REQUIREMENTS
----------------------------------------
```
google-adk==1.14.0
langchain-community==0.3.27
wikipedia==1.4.0
```

----------------------------------------
USAGE
----------------------------------------
1. Open Cloud Run Service URL
2. Use ADK Web Interface
3. Enter query like:
   - What is a black hole?
   - Explain galaxies

