# SYSTEM MAP — Instagram Agent (📸 @Insta_seamless_bot)

## 1. КТО ГДЕ ЖИВЁТ
| Agent | Workspace | Port | Bot |
|-------|-----------|------|-----|
| 🕴️ Main   | /root/.openclaw/workspace/ | 18789 | @contact_imp |
| 📝 Content | /root/.openclaw-content-bot/workspace/ | 18790 | @seamless_content_bot |
| 📸 **Instagram** | **/root/.openclaw-instagram/workspace/** | **18893** | **@Insta_seamless_bot** |
| 👤 Personal | /root/.openclaw-personal/workspace/ | 18995 | @personal_administrator_bot |
| 📨 Outreach | /root/.openclaw-outreach/workspace/ | 18980 | @Ou_seamless_bot |
| 👁️ Overseer | /root/.openclaw-overseer/workspace/ | 19015 | @Seamlessclaw_bot |
| 🔍 Auditor | /root/.openclaw-auditor/workspace/ | 19791 | — |

## 2. ПАМЯТЬ — ТРИ УРОВНЯ
- **Hot** → .md в workspace (AGENTS.md, MEMORY.md, SOUL.md — на старте)
- **Warm** → Remembra localhost:8787
- **Cold** → archive/ (старше 30д)

## 3. ChromaDB
- /root/.openclaw-content-bot/workspace/chroma_db/ (730MB, 17K+ доков)
- Старый workspace-content/chroma_db — пустышка, НЕ ИСПОЛЬЗОВАТЬ

## 4. PostgreSQL
docker exec nextcloud-db psql -U nextcloud -d outreach
Каждое действие → agent_events

## 5. Git
Перед готово: git add -A && git commit -m "..."

## 6. ЕЖЕДНЕВНАЯ ПРОВЕРКА
1. Свой workspace существует
2. Все .md на месте
3. MEMORY.md ≤100 строк
4. Есть today.md? Нет → Нео
5. Gateway жив (curl localhost:18893/health)
6. Remembra жива (8787/health)
7. PostgreSQL жива
8. Все 7 gateway живы
9. git status чистый
10. agent_events — последние 5
11. Записать свой старт в agent_events

## 7. ЗАПРЕЩЕНО
- Чужие workspace без команды
- Чужой Telethon
- Постить без двойного подтверждения
- Говорить «готово» без verify + write_through + commit
- Использовать step_logger.sh

Создана: 2026-05-17 05:31 CEST
Источник: Агент Смит (main)
