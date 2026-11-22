# Health Tracking

Десктопное приложение для здоровья: ИИ-ассистент здоровья, ИИ-психолог и проверка осанки по камере. Интерфейс — CustomTkinter, данные — SQLite.

## Модули

- `main.py` — главное окно и меню
- `ai_health_chat.py` — ИИ-ассистент здоровья (голос + текст)
- `ai_psychology_bot.py` — ИИ-психолог с анализом эмоций по камере
- `ai_posture_checker.py` — проверка осанки (YOLO pose)
- `database.py` — аккаунты и история в SQLite (`health_tracking.db` создаётся при запуске)

## Запуск

```bash
pip install -r requirements.txt
cd Health_Tracking
copy .env.example .env
# вставь свой ключ в .env: LLM7_API_KEY=...
python main.py
```

Ключ берётся только из переменной окружения `LLM7_API_KEY`. Никогда не вставляй ключ прямо в код — старые ключи из истории коммитов надо отозвать на стороне сервиса.

## Структура

```
Health_Tracking/
  main.py
  ai_health_chat.py
  ai_psychology_bot.py
  ai_posture_checker.py
  database.py
  models/
    yolov8n-pose.pt
  .env.example
```
