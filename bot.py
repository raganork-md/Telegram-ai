import os
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dedalus_labs import AsyncDedalus

# --- ENVIRONMENT VARIABLES ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEDALUS_API_KEY = os.getenv("DEDALUS_API_KEY")
MODEL_NAME = "anthropic/claude-opus-4-5"

# Setup AI Client (Runner-inu pakaram direct client upayogikkunnu)
client = AsyncDedalus(api_key=DEDALUS_API_KEY)

# Setup Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Logging setup
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# /start command
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.reply("Hello! Njan Claude AI Bot aanu. Enthekilum chodikku...")

# AI Response Handler
@dp.message()
async def handle_ai_response(message: types.Message):
    if not message.text:
        return

    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        # Direct API call with streaming enabled
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": message.text}],
            stream=True
        )

        full_response = ""
        async for chunk in response:
            # Chunk-il content undonnu check cheyyunnu
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content

        if full_response.strip():
            # Message length check (Telegram limit 4096)
            if len(full_response) > 4000:
                for i in range(0, len(full_response), 4000):
                    await message.answer(full_response[i:i+4000])
            else:
                await message.answer(full_response)
        else:
            await message.answer("AI-yil ninnu marupadi onnum kittiyilla.")
            
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer(f"Oru error sambhavichu: {str(e)}")

async def main():
    logging.info("Bot is starting...")
    if not TELEGRAM_BOT_TOKEN or not DEDALUS_API_KEY:
        logging.error("API Tokens missing!")
        return
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
        
