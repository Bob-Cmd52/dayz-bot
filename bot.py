import asyncio
import logging
import os
import requests

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TELEGRAM_TOKEN = os.getenv("8457388424:AAFjCZmfOhCiwLnQ8BRw-D42_y0kaEwGEcM")
OPENROUTER_API_KEY = os.getenv("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")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

SYSTEM_PROMPT = """
Ты — саркастичный оракул игры DayZ.
Делаешь короткие, мрачные, но смешные предсказания.
5–8 строк.
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
