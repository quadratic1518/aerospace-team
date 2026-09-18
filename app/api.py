"""HTTP API for Space Engineering Copilot."""

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .agent import answer, knowledge_base
from .tools import ALLOWED_TOOLS, run_calculator

app = FastAPI(title="Space Engineering Copilot", version="0.1.0")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home() -> str:
    """Provide a useful browser landing page instead of a 404 response."""
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Space Engineering Copilot</title>
<style>body{font-family:system-ui,sans-serif;max-width:42rem;margin:10vh auto;padding:0 1.5rem;line-height:1.55;color:#172033}a{color:#0563c1}</style>
</head><body><h1>Space Engineering Copilot</h1>
<p>The API is running. Use the interactive documentation to submit engineering questions and inspect supported endpoints.</p>
<p><a href="/docs">Open API documentation</a> &middot; <a href="/health">View service health</a></p>
<p><small>Preliminary engineering support only; independently verify all results.</small></p>
</body></html>"""


@app.get("/favicon.ico", include_in_schema=False, status_code=204)
def favicon() -> Response:
    """Avoid a noisy 404 when a browser automatically requests a favicon."""
    return Response(status_code=204)


class ChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=4000)


class ToolRequest(BaseModel):
    script: str
    arguments: list[str] = Field(default_factory=list, max_length=30)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "indexed_chunks": len(knowledge_base.chunks), "allowed_tools": sorted(ALLOWED_TOOLS)}


@app.post("/chat")
def chat(request: ChatRequest) -> dict:
    try:
        response, sources, calculations = answer(request.question)
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"answer": response, "sources": sources, "calculations": calculations, "disclaimer": "Preliminary engineering support only; independently verify all results."}


@app.post("/tools/execute")
def execute_tool(request: ToolRequest) -> dict:
    return run_calculator(request.script, request.arguments)
