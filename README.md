# Telegram Inline Genius Bot

Telegram Inline Bot на Python.

## Возможности

- Inline Mode
- Поиск песен через Genius
- До 24 результатов
- Кэширование
- Логирование
- Railway Ready
- Docker Ready

---

## Установка

```bash
git clone https://github.com/yourname/telegram-inline-genius-bot

cd telegram-inline-genius-bot
```

Создать виртуальное окружение

```bash
python -m venv .venv
```

Linux

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Установить зависимости

```bash
pip install -r requirements.txt
```

---

## Настройка

Создать

```
.env
```

по примеру

```
.env.example
```

---

## Переменные окружения

```
TELEGRAM_TOKEN=

GENIUS_TOKEN=

LOG_LEVEL=INFO

CACHE_TTL=3600

CACHE_SIZE=1024

GENIUS_SEARCH_LIMIT=24

GENIUS_TIMEOUT=15

GENIUS_RETRIES=3

GENIUS_RETRY_DELAY=2

INLINE_RESULTS_PER_PAGE=6
```

---

## Запуск

```bash
python bot.py
```

---

## Railway

Build Command

```bash
pip install -r requirements.txt
```

Start Command

```bash
python bot.py
```

---

## Docker

```bash
docker build -t telegram-inline-bot .
```

```bash
docker run --env-file .env telegram-inline-bot
```

---

## Структура

```
core/

handlers/

models/

services/

logs/

bot.py

requirements.txt

pyproject.toml
```

---

## Лицензия

MIT