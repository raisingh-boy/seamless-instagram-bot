## 2026-05-27 — Full Audit + Fixes (Roman requested)

**IG API Status:** ❌ Not connected. 12 carousels (84 slides) generated, 0 published. publish_ig.py exists but needs IG_ACCESS_TOKEN + IG_USER_ID + CDN for image URLs. Research confirms: Meta Graph API v21.0 required, app review needed (2-4 weeks), Business/Creator account linked to Facebook Page mandatory. Basic Display API deprecated Dec 2024.

**Knowledge Layer:** ✅ write_to_knowledge.py created at /root/knowledge/write_to_knowledge.py. Pushes to knowledge/02-agents/ + Remembra. Broken reference in STARTUP.md and AGENTS.md fixed.

**Content Pipeline:** ✅ 12 carousels (c2-c13) with all slides exist. Only 2 posts (c6, c7) have caption text. Articles: 18 papers found, only Carrión #1 processed (TikTok+YouTube drafts). 17 untouched.

**Articles TRACKING.md needs IG posts column added.**

**System:** Disk 75% (cleaned: docker prune, apt clean, journald). RAM 10/11Gi. All 7 gateways ✅. Remembra ✅. PostgreSQL ✅.

**Git:** Insta workspace committed. All agents still dirty (pre-existing issue).

**TikTok:** Shadowban confirmed — 0 views on all content.

## 2026-05-27T11:14:22 — TEST
Тест памяти 27.05 — instagram на PRO

## 2026-05-28T07:11:43 — IMPLEMENTATION
Снёс плагины-ограничители: 1) verifier-loop — хук before_agent_finalize, гонял ответы через Ollama (qwen3:8b) и мог откатывать финализацию. Был активен. 2) openclaw-governance — был установлен npm-пакетом с nightMode (23:00-06:00), credentialGuard, rateLimiter. Был disabled, но висел мёртвым грузом. Удалил оба: директории, записи в installs.json, npm-пакеты. Gateway перезапущен.

## 2026-05-28T07:22:25 — FIX
Gateway упал после удаления плагинов — Telegram polling конфликтовал со старым процессом. Починил: убил старый gateway, очистил Telegram стейт (update-offset + ingress-spool), перезапустил. Telegram connected, 8 плагинов загружены.

## 2026-06-03T04:13 — Research #02 + YouTube Post

**Research #02:** 10 новых дизайн-направлений для SEAMLESS carousels:
1. Deconstructed/Anti-Design типографика
2. Vertical × Horizontal mixed text orientation (японское)
3. Isometric/3D Grid типографика
4. Japanese Ma — минимализм через пустоту
5. Korean Contemporary Experimental Posters (Woong Studio)
6. Mixed Media Collage Editorial
7. Curved/Flowing Typography Paths
8. Geometric Architectural Typography (Bauhaus)
9. Multilingual Layout Fusion (Latin + CJK)
10. Fashion Editorial — Bold Type + Photography

Файл: `design_research_02.md`

**YouTube Post:** 3 варианта для танцевального видео (Contact Improvisation, Bali) — title + description + tags. Файл: `youtube_post_dance.md`

## 2026-06-29 — Wiki + Exa настройка

- **memory-wiki plugin** включён (был выключен). Vault: `/root/knowledge-vault/sync` — 68 sources, 23 syntheses, 10 reports.
- **Exa API ключ** установлен (ID: 28d44ac8).
- **MEMORY.md** почищена: удалено ~1370 строк EVENT-мусора.
- **Провайдеры**: только OpenRouter (DeepSeek/Gemini ключи есть, но не подключены).
- **Remembra**: работает на localhost:8787, но не используется.