"""Grounded chat loop with retrieval and OpenAI-compatible tool calling."""

from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from .retrieval import KnowledgeBase
from .tools import TOOL_DEFINITION, run_calculator

load_dotenv()
knowledge_base = KnowledgeBase()

SYSTEM_PROMPT = """You are Space Engineering Copilot for preliminary design only, not flight-certified analysis.
Use the supplied repository excerpts as the knowledge source. Cite every engineering claim with the supplied [source:path:line] markers.
For numerical calculations, use engineering_calculator rather than calculating from memory. State assumptions, units, limitations, and any missing inputs. Never claim a calculation was verified if no tool result was returned."""


def _client() -> OpenAI:
    key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL")
    if not key or not model or key == "replace-with-your-key" or model == "replace-with-your-model":
        raise ValueError("Set LLM_API_KEY and LLM_MODEL in .env (copy .env.example first).")
    return OpenAI(api_key=key, base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"))


def answer(question: str) -> tuple[str, list[str], list[dict]]:
    excerpts = knowledge_base.search(question)
    sources = [f"{chunk.source}:{chunk.line_start}" for chunk in excerpts]
    context = "\n\n".join(f"[source:{chunk.source}:{chunk.line_start}]\n{chunk.text}" for chunk in excerpts)
    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Repository excerpts:\n{context}\n\nQuestion: {question}"},
    ]
    calculations: list[dict] = []
    client = _client()
    model = os.environ["LLM_MODEL"]
    for _ in range(4):
        completion = client.chat.completions.create(model=model, messages=messages, tools=[TOOL_DEFINITION], tool_choice="auto")
        message = completion.choices[0].message
        messages.append(message.model_dump(exclude_none=True))
        if not message.tool_calls:
            return message.content or "No response generated.", sources, calculations
        for call in message.tool_calls:
            try:
                parameters = json.loads(call.function.arguments)
                result = run_calculator(parameters["script"], parameters["arguments"])
            except (KeyError, TypeError, json.JSONDecodeError) as exc:
                result = {"error": f"Invalid calculator request: {exc}"}
            calculations.append({"tool": call.function.name, "input": call.function.arguments, "output": result})
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
    return "I could not complete the requested calculation within the tool-call limit.", sources, calculations
