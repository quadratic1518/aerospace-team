"""Generate docs/index.html from RESEARCH_PAPER.md for GitHub Pages."""
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "RESEARCH_PAPER.md"
DOCS_DIR = ROOT / "docs"
HTML_PATH = DOCS_DIR / "index.html"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Space Engineering Pack — Research Paper</title>
  <style>
    :root {{
      --bg: #0f172a;
      --surface: #1e293b;
      --text: #e2e8f0;
      --muted: #94a3b8;
      --accent: #38bdf8;
      --border: #334155;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: Georgia, "Times New Roman", serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.7;
      padding: 2rem 1rem;
    }}
    .container {{
      max-width: 820px;
      margin: 0 auto;
      background: var(--surface);
      padding: 3rem 3.5rem;
      border-radius: 12px;
      border: 1px solid var(--border);
      box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    }}
    h1 {{ font-size: 1.75rem; margin-bottom: 1rem; color: #f1f5f9; line-height: 1.3; }}
    h2 {{ font-size: 1.35rem; margin: 2rem 0 0.75rem; color: var(--accent); border-bottom: 1px solid var(--border); padding-bottom: 0.4rem; }}
    h3 {{ font-size: 1.1rem; margin: 1.5rem 0 0.5rem; color: #cbd5e1; }}
    h4 {{ font-size: 1rem; margin: 1.25rem 0 0.4rem; color: #94a3b8; }}
    p {{ margin-bottom: 1rem; }}
    strong {{ color: #f1f5f9; }}
    a {{ color: var(--accent); }}
    blockquote {{
      border-left: 3px solid var(--accent);
      padding: 0.75rem 1rem;
      margin: 1rem 0;
      background: rgba(56,189,248,0.08);
      border-radius: 0 6px 6px 0;
      font-size: 0.95rem;
    }}
    code {{
      font-family: "Courier New", monospace;
      background: #0f172a;
      padding: 0.15em 0.4em;
      border-radius: 4px;
      font-size: 0.88em;
    }}
    pre {{
      background: #0f172a;
      padding: 1rem 1.25rem;
      border-radius: 8px;
      overflow-x: auto;
      margin: 1rem 0;
      border: 1px solid var(--border);
    }}
    pre code {{ background: none; padding: 0; font-size: 0.85em; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1rem 0;
      font-size: 0.92rem;
    }}
    th, td {{
      border: 1px solid var(--border);
      padding: 0.5rem 0.75rem;
      text-align: left;
    }}
    th {{ background: #0f172a; color: var(--accent); }}
    tr:nth-child(even) {{ background: rgba(15,23,42,0.5); }}
    ul, ol {{ margin: 0.75rem 0 1rem 1.5rem; }}
    li {{ margin-bottom: 0.35rem; }}
    hr {{ border: none; border-top: 1px solid var(--border); margin: 2rem 0; }}
    .footer {{
      text-align: center;
      margin-top: 2rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border);
      font-size: 0.85rem;
      color: var(--muted);
    }}
  </style>
</head>
<body>
  <div class="container">
{body}
    <div class="footer">
      SRM Institute of Science and Technology ·
      <a href="https://github.com/quadratic1518/aerospace-team">View on GitHub</a>
    </div>
  </div>
</body>
</html>
"""


def generate():
    md_text = MD_PATH.read_text(encoding="utf-8")
    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
    )
    DOCS_DIR.mkdir(exist_ok=True)
    HTML_PATH.write_text(HTML_TEMPLATE.format(body=body), encoding="utf-8")
    print(f"Generated: {HTML_PATH}")


if __name__ == "__main__":
    generate()
