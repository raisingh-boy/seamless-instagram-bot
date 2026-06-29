# MEMORY_LIMITS.md — Instagram Bot 📸

## File Size Limits

| File | Max Size | Max Lines | Notes |
|------|----------|-----------|-------|
| AGENTS.md | 15 KB | — | Boot protocol |
| MEMORY.md | 5 KB | 100 | Curated long-term |
| SOUL.md | 3 KB | — | Personality |
| IDENTITY.md | 1 KB | — | Who you are |
| HEARTBEAT.md | 2 KB | — | Periodic checks |
| today.md | 5 KB | 150 | Daily plan |
| AGENT_METHODOLOGY.md | 10 KB | — | Memory methodology |
| MEMORY_LIMITS.md | 3 KB | — | This file |
| SYSTEM_MAP.md | 10 KB | — | System architecture |
| Daily notes (memory/*.md) | 5 KB each | — | Raw logs |
| Post files | 800 bytes | — | One file per post |
| Bootstrap total | 40 KB | — | All startup files |

## Cleanup Rules
- MEMORY.md: review + clean weekly
- memory/*.md: move to archive/ after 30 days
- Post files: archive after publication
- Remove outdated decisions from MEMORY.md

## Event Sourcing
- agent_events format: INSERT INTO agent_events (agent, event_type, decision, reason, payload)
