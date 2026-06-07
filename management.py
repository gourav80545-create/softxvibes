import time
from pyrogram import filters
from config import Config
from database import db
from client import app

start_time = time.time()

@app.on_message(filters.command("ping"))
async def ping(client, message):
    start = time.time()
    msg = await message.reply_text("🏓 Pong!")
    ping = (time.time() - start) * 1000
    await msg.edit_text(f"🏓 Pong!\n⚡ {ping:.2f}ms")

@app.on_message(filters.command("stats"))
async def stats(client, message):
    stats_data = await db.get_stats()
    uptime = int(time.time() - start_time)
    hours = uptime // 3600
    
    await message.reply_text(f"""📊 STATS

👥 Users: {stats_data['users']}
💬 Groups: {stats_data['chats']}
🚫 Banned: {stats_data['banned_users']}

⏱ Uptime: {hours}h""")
