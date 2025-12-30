import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F

BOT_TOKEN = "8395704889:AAGB4rFWde8PjoQVzRc93dRGrjegu99AWlU"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎨 ساخت Meme", callback_data="meme_mode")],
        [InlineKeyboardButton(text="🚀 بازی راکت $XI", callback_data="game_rocket")]
    ])
    await message.answer(
        "🌌 خوش اومدی به XI Meme Generator! 🚀\n\n"
        "• ساخت memeهای futuristic و holographic با هوش مصنوعی\n"
        "• بازی پرتاب راکت $XI به ماه با جایزه\n\n"
        "#XItoTheMoon",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "meme_mode")
async def meme_mode(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎨 حالت ساخت Meme فعال شد!\n\n"
        "فقط prompt بنویس، مثلاً:\n"
        "XI rocket launching to the moon\n"
        "holographic neon XI logo in space\n\n"
        "meme خفن تحویل بگیر!"
    )

@dp.message(F.text & ~F.command)
async def generate_meme(message: Message):
    prompt = message.text.strip()
    
    full_prompt = f"{prompt}, highly detailed holographic futuristic art, neon blue glowing effects, dark cosmic background, ultra sharp, cinematic lighting, sci-fi atmosphere"
    
    await message.answer("🧠 در حال ساخت meme... (۱۰-۳۰ ثانیه) 🚀")

    try:
        response = requests.post(
            "https://fal.run/fal-ai/flux/schnell",
            headers={
                "Authorization": "Key e9f920d6-896f-4068-92d3-782df838676a:3fe3ef70848fb7e8eab0e9a96f5aa4dd",
                "Content-Type": "application/json"
            },
            json={
                "prompt": full_prompt,
                "image_size": "square_hd"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            image_url = data["images"][0]["url"]
            await message.answer_photo(
                image_url,
                caption=f"ممه $XI آماده شد! 🌌\nPrompt: {prompt}\n#XItoTheMoon"
            )
        else:
            await message.answer("خطا در ساخت meme – دوباره امتحان کن.")
    
    except Exception as e:
        await message.answer("مشکل فنی موقت! بعداً امتحان کن 😅")

@dp.callback_query(F.data == "game_rocket")
async def game_rocket(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 پرتاب راکت!", callback_data="launch")]
    ])
    await callback.message.edit_text(
        "🚀 بازی $XI Rocket Launch!\n\n"
        "راکت رو به ماه برسون و جایزه بگیر!\n\n"
        "دکمه پرتاب رو بزن!",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "launch")
async def launch(callback: types.CallbackQuery):
    await callback.message.edit_text("3... 2... 1... LAUNCH! 🚀\n\nراکت در حال حرکت به ماه...")
    await asyncio.sleep(3)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 BOOST NOW!", callback_data="win")]
    ])
    await callback.message.edit_text("الان بهترین زمان برای boost هست!!!", reply_markup=keyboard)

@dp.callback_query(F.data == "win")
async def win(callback: types.CallbackQuery):
    await callback.message.edit_text("🎉 تبریک! راکت $XI به ماه رسید!\n\nجایزه: meme ویژه $XI")
    await callback.message.answer_photo(
        "https://i.imgur.com/0k1QJ0T.jpg",  # می‌تونی لینک meme جایزه خودت بذاری
        caption="$XI to the Moon! 🌕🚀\n#XItoTheMoon"
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    print("$XI Meme Generator Bot در حال اجراست 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
