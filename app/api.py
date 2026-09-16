"""HTTP API for Space Engineering Copilot."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .agent import answer, knowledge_base
from .tools import ALLOWED_TOOLS, run_calculator

app = FastAPI(title="Space Engineering Copilot", version="0.1.0")


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
