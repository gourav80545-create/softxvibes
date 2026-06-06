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

@Client.on_message(filters.command("broadcast"))
@is_owner
async def broadcast(client, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a message!")
        return
    
    status = await message.reply_text("📢 Broadcasting...")
    users = await db.get_all_users()
    success = 0
    
    for user in users:
        try:
            await message.reply_to_message.copy(user['_id'])
            success += 1
        except:
            pass
    
    await status.edit_text(f"✅ Sent to {success} users!")
