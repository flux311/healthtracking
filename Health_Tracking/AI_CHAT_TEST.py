from openai import OpenAI

client = OpenAI(
    api_key="Mff3DwsfBGsZkvPEb/cZ1tpn4yozA/D9WEIOn3hXcIZ7H9DY9PZjdUuDGqUD9PxLVZ6K+4kwv68GpIC05/csnP++XETi3iDMZFnIhOHnrFhJhLOkpIk+09Lw3megget9PX82oyUMg6yE77+MOlY=",  # Или ваш токен с token.llm7.io
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