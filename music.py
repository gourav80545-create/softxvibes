from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db

@Client.on_message(filters.command("play"))
async def play(client, message):
    user_id = message.from_user.id
    
    if await db.is_banned(user_id):
        await message.reply_text("🚫 Banned!")
        return
    
    query = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else "Unknown"
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("▶️ Play", callback_data="music_play"),
         InlineKeyboardButton("⏸ Pause", callback_data="music_pause"),
         InlineKeyboardButton("⏭ Skip", callback_data="music_skip")],
        [InlineKeyboardButton("💖 Close", callback_data="close")]
    ])
    
    player_text = f"""🎶 STARTED STREAMING

➻ TITLE : {query}
➻ DURATION : 03:45
➻ REQUESTED BY : {message.from_user.mention}

{Config.DEVELOPER_CREDIT}

02:15 ━━━━━●━━━━━ 03:45"""
    
    await message.reply_text(player_text, reply_markup=keyboard)

@Client.on_message(filters.command("pause"))
async def pause(client, message):
    await message.reply_text("⏸ Paused!")

@Client.on_message(filters.command("skip"))
async def skip(client, message):
    await message.reply_text("⏭ Skipped!")
