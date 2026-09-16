"""Small, dependency-free retrieval layer for the engineering skill library."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = [ROOT / "README.md", ROOT / "RESEARCH_PAPER.md", *sorted((ROOT / "skills").glob("*/SKILL.md"))]
TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]{1,}")


@dataclass(frozen=True)
class Chunk:
    source: str
    line_start: int
    text: str


def _tokens(text: str) -> Counter[str]:
    return Counter(token.lower() for token in TOKEN_RE.findall(text))


def _chunks(path: Path, size: int = 1_800) -> list[Chunk]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    output: list[Chunk] = []
    buffer: list[str] = []
    start = 1
    for number, line in enumerate(lines, start=1):
        if buffer and (len("\n".join(buffer)) + len(line) > size or line.startswith("# ")):
            output.append(Chunk(path.relative_to(ROOT).as_posix(), start, "\n".join(buffer)))
            buffer, start = [], number
        buffer.append(line)
    if buffer:
        output.append(Chunk(path.relative_to(ROOT).as_posix(), start, "\n".join(buffer)))
    return output


class KnowledgeBase:
    def __init__(self) -> None:
        self.chunks = [chunk for path in SOURCE_FILES if path.exists() for chunk in _chunks(path)]

    def search(self, question: str, limit: int = 5) -> list[Chunk]:
        query = _tokens(question)
        scored = []
        for chunk in self.chunks:
            score = sum(min(count, _tokens(chunk.text)[token]) for token, count in query.items())
            if score:
                scored.append((score, chunk))
        return [chunk for _, chunk in sorted(scored, key=lambda item: item[0], reverse=True)[:limit]]
