#!/root/.openclaw/venv/bin/python3
"""Write-Through Protocol v2 — каждое решение → Remembra + agent_events + MEMORY.md
Использование: python3 write_through.py <agent> <type> <text>
  agent: main | content | instagram | personal | outreach | overseer | auditor
  type: architecture | decision | event | solution | plan | implementation
"""
import sys, os, json, datetime, subprocess

AGENTS = {
    "main":      "/root/.openclaw/workspace",
    "content":   "/root/.openclaw-content-bot/workspace",
    "instagram": "/root/.openclaw-instagram/workspace",
    "personal":  "/root/.openclaw-personal/workspace",
    "outreach":  "/root/.openclaw-outreach/workspace",
    "overseer":  "/root/.openclaw-overseer/workspace",
    "auditor":   "/root/.openclaw-auditor/workspace",
}

def usage():
    print("Usage: python3 write_through.py <agent> <type> <text>")
    print("  agent:", ", ".join(AGENTS.keys()))
    print("  type: architecture | decision | event | solution | plan | implementation")
    sys.exit(1)

if len(sys.argv) < 4:
    usage()

agent, event_type, text = sys.argv[1], sys.argv[2], sys.argv[3]
ws = AGENTS.get(agent)
if not ws: 
    print(f"Unknown agent: {agent}"); usage()

ts = datetime.datetime.now().isoformat()

# Remembra ключ из .remembra.json
rem_path = os.path.join(ws, ".remembra.json")
rem_key = ""
if os.path.isfile(rem_path):
    try:
        with open(rem_path) as f:
            rem_data = json.load(f)
            rem_key = rem_data.get("keys", {}).get(agent, "") or rem_data.get("api_key", "")
    except: pass

# 1. 📄 MEMORY.md
mem_md = os.path.join(ws, "MEMORY.md")
mem_entry = f"\n## {ts} — {event_type.upper()}\n{text}\n"
os.makedirs(os.path.dirname(mem_md), exist_ok=True)
with open(mem_md, "a") as f: f.write(mem_entry)

# 2. 📄 memory/YYYY-MM-DD.md
daily_dir = os.path.join(ws, "memory")
daily_file = os.path.join(daily_dir, f"{datetime.date.today().isoformat()}.md")
os.makedirs(daily_dir, exist_ok=True)
daily_entry = f"\n## {ts} — {event_type}\n{text}\n"
with open(daily_file, "a") as f: f.write(daily_entry)

# 3. 🧠 Remembra
try:
    import httpx
    httpx.post("http://127.0.0.1:8787/api/v1/memories",
               json={"content": text[:1000], "tags": [agent, event_type]},
               headers={"X-API-Key": rem_key}, timeout=5)
except Exception as e:
    print(f"Remembra error: {e}")

# 4. 🐘 agent_events (через Events API)
try:
    import httpx
    httpx.post("http://127.0.0.1:8094/event", json={
        "agent": agent,
        "event_type": event_type,
        "decision": f"write_through at {ts}",
        "reason": text[:200],
        "payload": {"text": text[:500], "via": "write_through.py"}
    }, timeout=5)
except Exception as e:
    print(f"agent_events error: {e}")

print(f"✅ {agent}: {event_type} — written to MEMORY.md + memory/ + Remembra + agent_events")
