import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from groq import Groq

# Вставь свои ключи сюда
TELEGRAM_TOKEN = "8755933295:AAFjkl20nwqez7TkoWedoDqq6zJ39P2DgFs"
GROQ_API_KEY = "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"

# Сначала создаём Telegram бота
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Потом создаём Groq клиента
client = Groq(api_key=GROQ_API_KEY)

# Словарь для хранения языка
user_language = {}

# Старт
@dp.message(CommandStart())
async def start(message: types.Message):
    lang_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🇬🇧 English"), KeyboardButton(text="🇷🇺 Русский")]],
        resize_keyboard=True
    )
    await message.answer("Choose language / Выберите язык", reply_markup=lang_keyboard)

# Обработка сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    if text == "🇬🇧 English":
        user_language[user_id] = "en"
        await message.answer("Language selected. Send your question.")
        return
    if text == "🇷🇺 Русский":
        user_language[user_id] = "ru"
        await message.answer("Язык выбран. Отправь свой вопрос.")
        return
    if user_id not in user_language:
        await message.answer("Please choose language first.")
        return

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are a helpful AI tutor helping students with school subjects."},
                {"role": "user", "content": text}
            ]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"Error: {e}"

    await message.answer(answer + "\n\nРеклама")

# Функция запуска
async def main():
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())