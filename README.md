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
copy .env.example .env
# вставь свой ключ в .env: LLM7_API_KEY=...
python main.py
```

Ключ берётся только из переменной окружения `LLM7_API_KEY`. Никогда не вставляй ключ прямо в код — старые ключи из истории коммитов надо отозвать на стороне сервиса.

## Структура

```
main.py
ai_health_chat.py
ai_psychology_bot.py
ai_posture_checker.py
database.py
assets/
  profile_avatar.png
  register_image.png
  health_assistant.png
  psychology_bot.png
  posture.png
  program_info_1.png
  program_info_2.png
  program_info_3.png
  speak_button.png
  psychology_rectangle.png
  frame_camera_off.png
  medcard_template.docx
Health_Tracking/
  models/
    yolov8n-pose.pt
.env.example
```
