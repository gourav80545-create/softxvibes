from pyrogram import filters
from config import Config
from database import db
from client import app

def is_owner(func):
    async def wrapper(client, message):
        if message.from_user.id != Config.OWNER_ID:
            await message.reply_text("❌ Only owner!")
            return
        return await func(client, message)
    return wrapper

@app.on_message(filters.command("gban"))
@is_owner
async def gban(client, message):
    user_id = message.reply_to_message.from_user.id
    reason = " ".join(message.text.split()[1:])
    await db.ban_user(user_id, reason)
    await message.reply_text(f"🚫 Banned!")

@app.on_message(filters.command("bluser"))
@is_owner
async def bluser(client, message):
    user_id = message.reply_to_message.from_user.id
    await db.banned_users.insert_one({"_id": user_id})
    await message.reply_text(f"🚫 Blacklisted!")
