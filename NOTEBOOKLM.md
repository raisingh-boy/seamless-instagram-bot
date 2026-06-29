# NotebookLM — доступ для Instagram бота

## Что установлено

- `notebooklm-py` в `/root/.openclaw-instagram/notebooklm-venv/`
- Playwright Chromium для браузерной аутентификации
- Активный профиль `instagram` с авторизацией

## Подключение

```bash
source /root/.openclaw-instagram/notebooklm-venv/bin/activate
notebooklm -p instagram list
```

## Доступные ноутбуки (9 шт.)

| ID (первые 8) | Название |
|---|---|
| `59960954` | Embodied Semantics — English Audio |
| `723ee2d6` | Embodied Semantics — Infographic EN |
| `9af09291` | Embodied Semantics and Language |
| `d834e5c4` | Тест: Мозг и Движение |
| `5573efa4` | Embodied Semantics — Paper |
| `cd8248e9` | Brain Signatures of Embodied Semantics — EN |
| `a264c8f5` | Brain Signatures of Embodied Semantics |
| `87da715f` | The Art of Indirect Suggestion in Clinical Hypnosis |
| `757d23e2` | The Persuadability Spectrum |

## Команды

```bash
# Выбрать ноутбук
notebooklm -p instagram use abc123

# Задать вопрос
notebooklm -p instagram ask "твой вопрос"

# Список ноутбуков
notebooklm -p instagram list

# Создать ноутбук
notebooklm -p instagram create "название"

# Удалить
notebooklm -p instagram delete abc123

# Статус (какой ноутбук активен)
notebooklm -p instagram status

# Смена языка
notebooklm -p instagram language set en

# Генерация инфографики
notebooklm -p instagram generate infographic
```

## Как получить контент для карусели

1. Выбрать нужный ноутбук: `notebooklm -p instagram use 59960954`
2. Спросить: `notebooklm -p instagram ask "Напиши 4-5 слайдов для Instagram карусели на тему..."`

## Формат постов

Формат, который использует Personal бот (запомнить!):
- Sans-Serif Bold (𝗦𝗘𝗔𝗠𝗟𝗘𝗦𝗦) для заголовков и ключевых фраз
- Основной текст — обычные символы
- Футер: SEAMLESS 2026 + Instagram | Website | Telegram ссылки
- Кириллицу выделять через **жирный** Telegram (sans-serif bold не поддерживает кириллицу)

## Аутентификация

Если сессия протухнет:
```bash
notebooklm -p instagram login
```
Откроется браузер — войти в Google-аккаунт.
