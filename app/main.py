from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.config import APP_NAME, GROQ_API_KEY, GROQ_MODEL
from app.schemas import AskRequest, AskResponse
from app.agents.team import build_research_team
from app.agents.tools import search_library

app = FastAPI(title=APP_NAME, version="1.0.0")
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

DISCLAIMER = (
    "This assistant is an educational coursework demonstration. Its sample library "
    "is limited and may be incomplete. Verify important findings using authoritative "
    "primary sources before relying on them."
)

@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "app_name": APP_NAME,
        "groq_configured": bool(GROQ_API_KEY),
        "model": GROQ_MODEL,
        "agents": ["Query Analyzer", "Research Agent", "Answer Reviewer"],
    }

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    if not GROQ_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="GROQ_API_KEY is not configured. Add your key to the .env file.",
        )
    try:
        team = build_research_team()
        result = team.run(request.question)
        answer = getattr(result, "content", None) or str(result)
        library_results = search_library(request.question)
        sources = []
        for line in library_results.splitlines():
            if line.startswith("Source: "):
                sources.append(line.split("|")[0].replace("Source: ", "").strip())
        return AskResponse(
            status="success",
            question=request.question,
            answer=str(answer),
            sources=sources,
            disclaimer=DISCLAIMER,
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Agent processing failed: {exc}") from exc
