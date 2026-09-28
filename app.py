"""FastAPI front end for opnames.

Run:  uv run uvicorn app:app --reload
Then: http://127.0.0.1:8000/            (click-for-another page)
      http://127.0.0.1:8000/names?style=ww2&count=5
      http://127.0.0.1:8000/docs         (Swagger UI)
"""
from dataclasses import asdict
from enum import Enum

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

import opnames

app = FastAPI(title="Op Name Generator", version="1.0")


class Style(str, Enum):
    modern = "modern"
    ww2 = "ww2"
    exercise = "exercise"


@app.get("/styles")
def styles() -> list[str]:
    return list(opnames.STYLES)


@app.get("/names")
def names(
    style: Style = Style.modern,
    count: int = Query(1, ge=1, le=50),
    seed: int | None = None,
):
    try:
        return [asdict(c) for c in opnames.generate(style.value, count, seed)]
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.get("/", response_class=HTMLResponse)
def index(style: Style = Style.modern):
    c = opnames.generate(style.value)[0]
    links = " · ".join(f'<a href="/?style={s}">{s}</a>' for s in opnames.STYLES)
    return f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{c.short}</title>
<style>
 body{{font-family:"Courier New",monospace;background:#1f2a1c;color:#e8e2c8;
 display:grid;place-items:center;min-height:100vh;margin:0;text-align:center}}
 .stamp{{border:3px solid #b3312c;color:#b3312c;padding:.2em .6em;display:inline-block;
 transform:rotate(-4deg);letter-spacing:.2em;font-weight:bold}}
 h1{{font-size:clamp(2rem,9vw,4.5rem);letter-spacing:.08em;margin:.4em 0}}
 a{{color:#c9c08f}}
 .wrap{{max-width:36rem;padding:1.5rem 1rem}}
 .blurb{{font-size:.95rem;line-height:1.5;color:#c9c3a6;margin:0 0 2rem;
 border-bottom:1px dashed #5a6450;padding-bottom:1.2rem}}
</style></head><body><div class="wrap">
<p class="blurb">Generates code names in the style of British military operations
and exercises: an obscure single word like modern MOD operations, a racecourse-or-hunt
name in the Second World War tradition, or an adjective-and-noun training exercise.
Names of real operations are left out. Pick a style below and hit
&ldquo;Generate another&rdquo; until one sticks.</p>
<div class="stamp">OFFICIAL-SENSITIVE</div>
<p>{c.full.split()[0].upper()}</p><h1>{c.name}</h1>
<p><a href="/?style={style.value}">Generate another</a></p>
<p><small>{links}</small></p>
</div></body></html>"""
