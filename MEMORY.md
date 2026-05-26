## 2026-05-17T05:32 — AUDIT
Full system audit. Created AGENT_METHODOLOGY.md, MEMORY_LIMITS.md, SYSTEM_MAP.md.
Weak spots: 0 posts, no IG API connection, broken generators.

## 2026-05-17T05:38 — ATTEMPTED FIX
Tried rewriting gen_carousel_2.py from playwright to Pillow. **Files not found/not committed** — confirmed missing 2026-05-18.

## 2026-05-18T05:52 — WEAK SPOT AUDIT
- **Critical:** All gen_carousel_*.py files GONE. carousel_photo/ GONE.
- **Critical:** IG API not connected — 0 posts published since creation.
- **Action:** Need complete carousel generator rebuild + IG API setup.
- **Git:** Cleaned up, committed with today's audit.

## 2026-05-18T05:53:04.008818 — EVENT
Weak spots found on 2026-05-18: 1) gen_carousel_*.py missing — regression from 2026-05-17, 2) carousel_photo/ missing, 3) IG API disconnected, 4) 0 posts, 5) MEMORY.md had false entries — fixed, 6) today.md created, 7) git committed

## 2026-05-18T07:45 — IMPLEMENTATION
Созданы Carousel #6 (Dance as Medicine) и Carousel #7 (Your Body Knows First).
- Показывать фото Roman на утверждение перед генерацией!
- Посты содержат строку: Ph: @andrey_berezkin
- Все gen_carousel_*.py (2-7) живут в /root/.openclaw-instagram/ (не workspace/)
- carousel_photo/ там же

## WORKFLOW — Как Работаем
1. Roman даёт тему → research
2. Показать фото на утверждение
3. Сгенерировать карусели (Pillow, 7 слайдов, 1080×1350)
4. Пост: чистый текст, без HTML, без таймингов
5. Добавить Ph: @andrey_berezkin
6. Отправить слайды + текст в Telegram

## 2026-05-18T08:09:07.210787 — DECISION
WORKFLOW записан: 1) Roman даёт тему 2) Показываю фото на утверждение 3) Генерация карусели 4) Пост без HTML 5) Ph: @andrey_berezkin 6) Отправка в Telegram. Фото обновлены на утверждённые (7O0A4626.jpg и 7O0A5442.jpg). Посты обновлены.

## 2026-05-25 — Linguistics + Movement Research Day
Roman дал новые направления:
- **Видео:** Скачал `reel_DXZbb-liuwc` (CI partnering, karpaanastasya x Gymnasium Bali) — TikTok-ready
- **TikTok:** 0 показов — возможно shadowban из-за номера телефона
- **Новая тема:** Психолингвистика + движение/танец. Семантика движения. Тело как язык. Звук и движение.
- **Найдено 18 статей** (список в memory/2026-05-25.md)
- **План:** Работать по блокам статей — посты + скрипты диктовок для TikTok/YouTube
- **Главные статьи на старт:**
  1. Carrión (2026) — Meaning Construal in Contemporary Dance (когнитивная лингвистика + танец)
  2. Arbib & Cuccio (2026) — The body in language, the language beyond the body
  3. Sanna (2025) — Proprioceptive resonance and multimodal semiotics

## 2026-05-25T08:39:27.024032 — DECISION
2026-05-25: Найдено 18 статей по теме психолингвистика+движение (список сохранён в articles/linguistic_movement_papers.md). Скачан и сконвертирован reel_DXZbb-liuwc. План: работа по блокам статей — посты + скрипты диктовок.

## 2026-05-26T04:33:08.438650 — EVENT
старт по команде Нео

## 2026-05-26T04:34 — WEAK SPOT AUDIT + FIX
Полный аудит системы по команде Нео.

### Слабые места (критические):
1. ❌ **IG API не подключён** — 12 каруселей с 84 слайдами + 6 постов готовы, НО 0 опубликовано
2. ❌ **Knowledge layer tool не существует** — dead reference в STARTUP.md (`/root/knowledge/write_to_knowledge.py`)
3. ❌ **Нет прогресса по articles Carrión/Arbib/Sanna** — остановлено с 25 мая

### Слабые места (средние):
4. ⚠️ **Git dirty** — .gitignore не было в корне репозитория
5. ❌ **TikTok shadowban** — 2 reels конвертированы, 0 показов

### Что сделано:
- ✅ .gitignore создан (исключает сгенерированные ассеты, .env, токены)
- ✅ today.md создан (сессия)
- ✅ publish_ig.py написан — готов к подключению, ждёт credentials
- ✅ agent_events записан
- ✅ Исправлены записи в MEMORY.md

## 2026-05-26T04:35:40.495494 — AUDIT
полный аудит 2026-05-26: найдены слабые места (IG API не подключён, knowledge tool dead, нет прогресса по articles). Созданы .gitignore, today.md, publish_ig.py. Проведена верификация.
