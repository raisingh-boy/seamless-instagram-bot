# 2026-05-26 — Instagram Bot

## Старт по команде Нео
- Проведён полный аудит системы
- Все 7 gateway ✅
- PostgreSQL ✅, Remembra ✅
- self_scan: 25/27 ✅ (2 weak spots)

## Аудит — Слабые места
1. ❌ IG API не подключён — 12 каруселей сгенерировано, 0 опубликовано
2. ❌ Knowledge layer tool не существует (broken reference в STARTUP.md + AGENTS.md)
3. ⚠️ Git dirty — нет .gitignore в корне
4. ❌ Прогресс по статьям Carrión/Arbib/Sanna остановлен с 25 мая
5. ❌ TikTok shadowban — 0 views
6. ⚠️ MEMORY.md обновлена с новыми weak spots

## План
- [x] .gitignore создан
- [x] today.md создан
- [x] IG publishing script готов (ждёт credentials)
- [ ] Подключить IG API через Meta Developer App
- [ ] Возобновить работу по linguistics + movement
