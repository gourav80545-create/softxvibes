from pyrogram import Client, filters
from config import Config
from database import db

def is_owner(func):
    async def wrapper(client, message):
        if message.from_user.id != Config.OWNER_ID:
            await message.reply_text("❌ Only owner!")
            return
        return await func(client, message)
    return wrapper

@Client.on_message(filters.command("auth"))
@is_owner
async def auth(client, message):
    user_id = message.reply_to_message.from_user.id
    await db.users.update_one({"_id": user_id}, {"$set": {"authorized": True}})
    await message.reply_text(f"✅ Authorized!")

@Client.on_message(filters.command("authusers"))
@is_owner
async def auth_users(client, message):
    users = await db.users.find({"authorized": True}).to_list(None)
    text = "✅ AUTHORIZED:\n\n"
    for user in users:
        text += f"`{user['_id']}`\n"
    await message.reply_text(text)
