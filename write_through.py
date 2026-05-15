#!/root/.openclaw/venv/bin/python3
"""Write-Through Protocol для Instagram"""
import os, json, subprocess
from datetime import datetime

WORKSPACE = "/root/.openclaw-instagram/workspace"
REMEMBRA_KEY = "rem_RZGGb6Nk8B6YdtQB0Pv6Z3lqLEBrOD5RAxqDNqz8mYQ"

def get_daily_path():
    return os.path.join(WORKSPACE, "memory", f"{datetime.now().strftime('%Y-%m-%d')}.md")

def write(event_type: str, content: str, tags: list = None):
    ts = datetime.now().isoformat()
    tags_str = ", ".join(tags) if tags else ""
    entry = f"\n## {ts} — {event_type}\n{content}\n"
    if tags_str:
        entry = entry.rstrip() + f"\nTags: {tags_str}\n"
    path = get_daily_path()
    with open(path, "a") as f:
        f.write(entry)
    # Remembra
    try:
        import httpx
        httpx.post("http://127.0.0.1:8787/api/v1/memories", 
                   json={"content": content[:500], "tags": tags or []},
                   headers={"X-API-Key": REMEMBRA_KEY}, timeout=5)
    except:
        pass
    print(f"✅ Written: {event_type}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        write(sys.argv[1], sys.argv[2], sys.argv[3:] if len(sys.argv) > 3 else None)
