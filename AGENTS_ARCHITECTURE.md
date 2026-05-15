# Полная архитектура системы — 14.05.2026 (финал)

## 1. Gateways

| Агент | Порт | HOME | Workspace | Telegram | DeepSeek Key |
|-------|------|------|-----------|----------|-------------|
| **Main** 🕴️ | 18789 | `/root/.openclaw/` | `/root/.openclaw/workspace/` | @Seamless_movement (Telethon) + @Seamless_movement_vps_bot | sk-0b52... (boss 89) |
| **Content-bot** 📝 | 18790 | `/root/.openclaw-content-bot/` | `/root/.openclaw-content-bot/workspace/` | @seamless_content_bot | sk-a883... |
| **Instagram** 📸 | 18893 | `/root/.openclaw-instagram/` | `/root/.openclaw-instagram/workspace/` | @Insta_seamless_bot | sk-6caa... |
| **Personal** 🗓️ | 18995 | `/root/.openclaw-personal/` | `/root/.openclaw-personal/workspace/` | @personal_administrator_bot | sk-bee6... |
| **Outreach** 📬 | 18980 | `/root/.openclaw-outreach/` | `/root/.openclaw-outreach/workspace/` | @Ou_seamless_bot | sk-3c2c... |
| **Overseer** 👁️ | 19015 | `/root/.openclaw-overseer/` | `/root/.openclaw-overseer/workspace/` | — | sk-4df9... |
| **Auditor** 🔍 | 19791 | `/root/.openclaw-auditor/` | `/root/.openclaw-auditor/workspace/` | — | sk-19b6... |

## 2. Системные сервисы

| Сервис | Порт | Где | Для кого |
|--------|------|-----|----------|
| Remembra | 8787 | Docker (host), Ollama | Все |
| Ollama | 11434 | systemd | Remembra (nomic-embed-text) |
| Qdrant | 6333/6334 | Docker (host), 768 dims | Remembra |
| Outreach API | 8790 | systemd (outreach-api.service) | Outreach |
| Queue Worker | — | systemd (queue-worker.service) | Outreach |
| nginx | 80/443 | systemd | Прокси /webhook/ → 8790 |
| Nextcloud | 8080 | Docker | Бэкапы |
| Mail | 25/143/465/587/993 | Docker (mailserver) | Почта агентов |

## 3. Cron задачи (self-check)

| Агент | Крон | Расписание | Задача |
|-------|------|-----------|--------|
| **Main** | gateway-health-check | каждые 30 мин | проверить 8 gateways |
| **Main** | docs-refresh | 06:00 CEST | обновить документацию |
| **Main** | scraper-morning-check | 08:00 Bali | статус scraper |
| **Main** | scraper-late-check | 10:00 Bali | статус scraper |
| **Main** | backup-* | 08:00/20:00 Bali | бэкапы |
| **Overseer** | overseer-check | каждые 30 мин | проверить gateways |
| **Auditor** | auditor-check | каждые 30 мин | аудит системы |
| **Outreach** | 13 кронов | разное | parse, backup, cycle, inbox, health |

## 4. API endpoints

| Эндпоинт | Порт | Для кого | Описание |
|----------|------|----------|----------|
| /webhook/parse | 8790 (nginx) | Outreach | запуск scraper |
| /webhook/daily-cycle | 8790 (nginx) | Outreach | дневной цикл |
| /webhook/check-inbox | 8790 (nginx) | Outreach | проверка входящих |
| /webhook/daily-report | 8790 (nginx) | Outreach | ежедневный отчёт |
| /webhook/backup | 8790 (nginx) | Outreach | бэкап |
| /webhook/response | 8790 (nginx) | Outreach | обработка ответов |
| /webhook/full-catchup | 8790 (nginx) | Outreach | полный сбор |
| /health | у всех gateways | проверка | статус |

## 5. Хранилища (где что лежит)

| Данные | Где | Тип |
|--------|-----|-----|
| agent_events (решения) | PostgreSQL (172.18.0.3:5432) | Таблица outreach.agent_events |
| Лиды, очередь, диалоги | PostgreSQL | Таблицы outreach.* |
| ChromaDB (контент) | /root/.openclaw-content-bot/workspace/chroma_db/ | Векторная (6 коллекций) |
| Remembra (память) | Qdrant (localhost:6333) + SQLite | Векторная + граф (Ollama) |
| Сессии agents | /root/.openclaw/agents/*/sessions/ | JSONL файлы |
| Бэкапы | Nextcloud (8080) + /root/.openclaw/backups/ | tar.gz |

## 6. Жёсткие правила

1. НЕ трогать конфиги без приказа
2. Каждый шаг — спрашивать
3. Никакой инициативы
4. НЕ лезть в чужие workspace/HOME
5. НЕ трогать чужие gateway/port
6. НЕ переносить то что работает
7. Перед любым действием — research
8. Каждое решение → agent_events

## 7. Ключевые события дня (14.05.2026)

1. Remembra → Ollama (OpenAI quota кончилась)
2. Миграция HOME — каждый агент в своей корневой папке
3. DeepSeek ключи — каждому свой
4. Content-bot workspace перенесён в /root/.openclaw-content-bot/
5. Instagram/Personal/Overseer/Auditor — workspace в своих HOME
6. Event Sourcing протокол — все решения в agent_events
7. Research Before Action — сначала поиск, потом действие
8. Exa ключ добавлен в конфиг
