#!/usr/bin/env python3
"""Self-Scan — проверка слабых мест при пробуждении. Запускается из Session Boot Protocol."""
import subprocess, json, sys, os
from datetime import datetime, timezone

CHECKS = []
PASS = 0
FAIL = 0

def check(name, ok, detail=""):
    global PASS, FAIL
    status = "✅" if ok else "❌"
    CHECKS.append(f"{status} {name}: {detail if not ok else 'ok'}")
    if ok: PASS += 1
    else: FAIL += 1

def run(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout, r.returncode
    except: return "", 1

def http(url, timeout=5):
    try:
        import urllib.request
        r = urllib.request.urlopen(url, timeout=timeout)
        return r.status
    except: return 0

# 1. Gateways
for port, name in [
    (18789, "main"), (18790, "content"), (18893, "instagram"),
    (18995, "personal"), (18980, "outreach"), (19015, "overseer"),
    (19791, "auditor")
]:
    code = http(f"http://127.0.0.1:{port}/health")
    check(f"gateway:{name} (:{port})", code == 200, f"HTTP {code}")

# 2. Services
for s in ["memory-guardian", "agent-events-api", "kg-memory", "nginx"]:
    out, rc = run(f"systemctl is-active {s}")
    check(f"service:{s}", out.strip() == "active", out.strip())

# 3. Plugins
out, rc = run("openclaw plugins list 2>/dev/null")
check("plugin:governance", "Governance" in out, "not found")
check("plugin:verifier-loop", "verifier" in out, "not found")

# 4. Loop detection on all gateways
for path in ["/root/.openclaw/openclaw.json"] + [f"/root/.openclaw-{a}/openclaw.json"
    for a in ["content-bot", "instagram", "personal", "outreach", "overseer", "auditor"]]:
    port_name = path.split("/")[2] if "/" in path else path
    try:
        with open(path) as f:
            d = json.load(f)
        ld = "loopDetection" in json.dumps(d.get("tools", {}))
        check(f"loopdetect:{path.split('/')[2]}", ld, "not configured")
    except: check(f"loopdetect:{path}", False, "can't read")

# 5. Verifier model
out, rc = run("curl -s http://127.0.0.1:11434/api/tags")
try:
    models = json.loads(out).get("models", [])
    has_qwen = any("qwen" in m.get("name", "") for m in models)
    check("model:qwen2.5:3b", has_qwen, "not found")
except: check("model:ollama", False, "not responding")

# 6. Governance config
try:
    with open("/root/.openclaw/plugins/openclaw-governance/config.json") as f:
        g = json.load(f)
    facts = len(g.get("outputValidation", {}).get("factRegistries", [{}])[0].get("facts", []))
    rules = g.get("responseGate", {}).get("rules", [])
    check("governance:facts", facts >= 28, f"{facts} facts")
    check("governance:response-gate", len(rules) >= 2, f"{len(rules)} rules")
except: check("governance:config", False, "can't read")

# 7. RAM
try:
    with open("/proc/meminfo") as f:
        mem = f.read()
    avail = int([l for l in mem.split("\n") if "MemAvailable" in l][0].split()[1])
    total = int([l for l in mem.split("\n") if "MemTotal" in l][0].split()[1])
    pct = round((total - avail) / total * 100)
    ok = avail > 500_000  # 500MB min
    check(f"ram:{pct}% used", ok, f"{avail//1024}MB free / {total//1024}MB total")
except: check("ram", False)

# 8. Git
out, rc = run("cd /root/.openclaw/workspace && git diff --stat 2>/dev/null")
check("git:clean", not out.strip(), "uncommitted changes")

# 9. Backup
out, rc = run("ls /root/backups/*.tar.gz 2>/dev/null | wc -l")
try:
    n = int(out.strip())
    check("backup:exists", n > 0, f"{n} backups")
except: check("backup", False, "no backups")

# 10. Write-Through
check("write-through:script", os.path.isfile("/root/openclaw-guardian/write_through.py"), "missing")

# Итог
print(f"\n=== SELF-SCAN: {PASS}✅ / {FAIL}❌ ===")
if FAIL == 0:
    print("VERDICT: PASS ✅")
else:
    print(f"VERDICT: FAIL — {FAIL} weaknesses found ⚠️")

for c in CHECKS:
    print(c)
