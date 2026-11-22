from openai import OpenAI
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

client = OpenAI(
    api_key=os.environ.get("LLM7_API_KEY"),  # Или ваш токен с token.llm7.io
    base_url="https://api.llm7.io/v1"
)

response = client.chat.completions.create(
    model="fast",  # Быстрая и умная модель
    messages=[
        {"role": "system", "content": "Ты — медицинский помощник. Не ставишь диагнозы, но даёшь рекомендации."},
        {"role": "user", "content": "У меня болит голова, текут ручьём прозрачные не густые сопли, болит горло и я постоянно чихаю, что это может быть?"}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)