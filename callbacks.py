from pyrogram import Client, filters

@Client.on_callback_query(filters.regex("music_play"))
async def music_play(client, callback_query):
    await callback_query.answer("▶️ Playing...")

@Client.on_callback_query(filters.regex("music_pause"))
async def music_pause(client, callback_query):
    await callback_query.answer("⏸ Paused...")

@Client.on_callback_query(filters.regex("close"))
async def close(client, callback_query):
    await callback_query.message.delete()
