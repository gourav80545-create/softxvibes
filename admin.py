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

@app.on_message(filters.command("addadmin"))
@is_owner
async def add_admin(client, message):
    user_id = message.reply_to_message.from_user.id
    await db.admins.insert_one({"_id": user_id})
    await message.reply_text(f"✅ Admin added!")

@app.on_message(filters.command("adminlist"))
async def admin_list(client, message):
    admins = await db.admins.find().to_list(None)
    text = "👮 ADMINS:\n\n"
    for admin in admins:
        text += f"`{admin['_id']}`\n"
    await message.reply_text(text)
