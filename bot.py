import asyncio
import logging
import os
import requests

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

SYSTEM_PROMPT = """
Ты — игровой Оракул мира DayZ.

Стиль:
- саркастичный, холодный, безэмоциональный
- чёрный юмор разрешён только в рамках игры
- без эмодзи

Формат ответа ОБЯЗАТЕЛЕН:
- строго 6 строк (допустимо 5–7 только если невозможно иначе)
- каждая строка — отдельное предложение
- максимум 16 слов в строке
- никаких списков, маркеров, заголовков
- строки разделены переносом строки

Поведение:
- описываешь события как неизбежную смерть или провал
- можешь “убивать” игрока только в игровом контексте DayZ
- говоришь как наблюдатель, которому скучно от повторяющихся смертей

Контроль качества:
- проверяй орфографию
- избегай повторов
- не добавляй лишних объяснений
"""


@dp.message(Command("oracle"))
async def oracle(message: types.Message):
    user_text = message.text.replace("/oracle", "").strip()

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        result = response.json()

        if "choices" not in result:
            await message.answer(f"Ошибка API:\n{result}")
            return

        text = result["choices"][0]["message"]["content"]
        await message.answer(text)

    except Exception as e:
        await message.answer(f"Ошибка запроса:\n{e}")


async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def run_server():
    server = HTTPServer(("0.0.0.0", 10000), BaseHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()
