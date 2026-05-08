import os
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dedalus_labs import AsyncDedalus, DedalusRunner

# --- ENVIRONMENT VARIABLES ---
# Render-ile 'Environment' tab-il ee keys nalkunnu ennu urappu varuthuka
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEDALUS_API_KEY = os.getenv("DEDALUS_API_KEY")
MODEL_NAME = "anthropic/claude-opus-4-5"

# Setup AI Client
ai_client = AsyncDedalus(api_key=DEDALUS_API_KEY)
runner = DedalusRunner(ai_client)

# Setup Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Logging setup
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# /start command
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.reply("Hello! Njan Claude AI Bot aanu. Enthekilum chodikku...")

# AI Response Handler (With Streaming Fix)
@dp.message()
async def handle_ai_response(message: types.Message):
    if not message.text:
        return

    # User-inu 'typing' status kanikkan
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        full_response = ""
        
        # Anthropic models-inu streaming logic (Error 400 ozhivakkan)
        async for chunk in runner.stream(
            input=message.text,
            model=MODEL_NAME,
        ):
            if chunk.content:
                full_response += chunk.content

        # Final output ayakkunnu
        if full_response.strip():
            # Telegram-il 4096 characters-il kooduthal message ayakkan pattilla
            # Athu kondulla cheriya oru check
            if len(full_response) > 4000:
                for i in range(0, len(full_response), 4000):
                    await message.answer(full_response[i:i+4000])
            else:
                await message.answer(full_response)
        else:
            await message.answer("AI-yil ninnu response onnum kittiyilla.")
            
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer("Oru error sambhavichu. Bot settings check cheyyuka.")

async def main():
    logging.info("Bot is starting...")
    # Token check
    if not TELEGRAM_BOT_TOKEN or not DEDALUS_API_KEY:
        logging.error("API Tokens missing in Environment Variables!")
        return
        
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
        
