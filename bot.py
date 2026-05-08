import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dedalus_labs import AsyncDedalus, DedalusRunner

# 1. API Keys (Ivide ningalude keys nalkuka)
TELEGRAM_BOT_TOKEN = "8708879724:AAHIj2riGN3_JT1i9W6uihzlw25SUxo7Lb8"
DEDALUS_API_KEY = "dsk-test-775d591fed32-3c896b1a4e10701a880b60017a3d33a1"

# 2. Setup AI Client
ai_client = AsyncDedalus(api_key=DEDALUS_API_KEY)
runner = DedalusRunner(ai_client)

# 3. Setup Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Start Command
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.reply("Hello! Njan Claude AI Bot aanu. Enthekilum chodikku...")

# Message Handler (AI logic)
@dp.message()
async def handle_ai_response(message: types.Message):
    if not message.text:
        return

    # Typing status kanikkan (Bot is typing...)
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        # AI-yodu chodyam chodikkunnu
        response = await runner.run(
            input=message.text,
            model="anthropic/claude-opus-4-5",
        )
        
        # Marupadi ayakkunnu
        await message.answer(response.final_output)
        
    except Exception as e:
        await message.answer("Sry, entho error patti. Pinne sremikku.")
        print(f"Error: {e}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
