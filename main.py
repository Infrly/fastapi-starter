"""A minimal FastAPI app that deploys on Infrly with no configuration.

Infrly runs `uvicorn main:app --host 0.0.0.0 --port $PORT`. If you add a
PostgreSQL database to the project and set DATABASE_URL, the home page
shows that the app can reach it.
"""

import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Infrly FastAPI starter")


def database_status() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        return "No database yet. Add PostgreSQL to this project and set DATABASE_URL."
    try:
        import psycopg

        with psycopg.connect(url, connect_timeout=5) as conn:
            version = conn.execute("select version()").fetchone()[0]
        return f"Connected: {version.split(',')[0]}"
    except Exception as e:  # show the reason instead of failing the page
        return f"Couldn't connect to the database: {type(e).__name__}"


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>FastAPI on Infrly</title>
<style>body{{font:16px/1.6 system-ui,sans-serif;max-width:640px;margin:12vh auto;padding:0 20px;color:#1f1f1d}}
code{{background:#f1f0ec;padding:2px 6px;border-radius:4px}}</style></head><body>
<h1>Your FastAPI app is live 🎉</h1>
<p>Edit <code>main.py</code>, push to GitHub, and Infrly deploys the new version.</p>
<p><b>Database:</b> {database_status()}</p>
<p>API docs: <a href="/docs">/docs</a> · Health check: <a href="/health">/health</a></p>
</body></html>"""
