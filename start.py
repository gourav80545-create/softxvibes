import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config, Messages, HelpTexts
from database import db

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start"))
async def start_handler(client: Client, message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username or "Unknown"
        
        await db.add_user(user_id, username)
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("➕ Add Me", url=f"https://t.me/{(await client.get_me()).username}?startgroup=new"),
                InlineKeyboardButton("📚 Commands", callback_data="help")
            ],
            [
                InlineKeyboardButton("💬 Support", url="https://t.me/softxvibessupport"),
                InlineKeyboardButton("📢 Updates", url="https://t.me/softxvibesupdates")
            ]
        ])
        
        await message.reply_text(Messages.START_MESSAGE, reply_markup=keyboard)
        logger.info(f"✨ User started: {user_id}")
    except Exception as e:
        logger.error(f"Error: {e}")

@Client.on_callback_query(filters.regex("help"))
async def help_handler(client: Client, callback_query):
    try:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Admin", callback_data="help_admin"),
                InlineKeyboardButton("Auth", callback_data="help_auth"),
                InlineKeyboardButton("Broadcast", callback_data="help_broadcast")
            ],
            [
                InlineKeyboardButton("Music", callback_data="help_music"),
                InlineKeyboardButton("Moderation", callback_data="help_mod"),
                InlineKeyboardButton("Management", callback_data="help_mgmt")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="start")
            ]
        ])
        
        await callback_query.edit_message_text(Messages.HELP_MESSAGE, reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error: {e}")

@Client.on_callback_query(filters.regex("help_admin"))
async def help_admin(client: Client, callback_query):
    try:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="help")]])
        await callback_query.edit_message_text(HelpTexts.ADMIN, reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error: {e}")

@Client.on_callback_query(filters.regex("help_auth"))
async def help_auth(client: Client, callback_query):
    try:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="help")]])
        await callback_query.edit_message_text(HelpTexts.AUTH, reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error: {e}")

@Client.on_callback_query(filters.regex("help_broadcast"))
async def help_broadcast(client: Client, callback_query):
    try:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="help")]])
        await callback_query.edit_message_text(HelpTexts.BROADCAST, reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error: {e}")

@Client.on_callback_query(filters.regex("help_music"))
async def help_music(client: Client, callback_query):
    try:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="help")]])
        await callback_query.edit_message_text(HelpTexts.MUSIC, reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error: {e}")

@Client.on_callback_query(filters.regex("help_mod"))
async def help_mod(client: Client, callback_query):
    try:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="help")]])
        await callback_query.edit_message_text(HelpTexts.MODERATION, reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error: {e}")

@Client.on_callback_query(filters.regex("help_mgmt"))
async def help_mgmt(client: Client, callback_query):
    try:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="help")]])
        await callback_query.edit_message_text(HelpTexts.MANAGEMENT, reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error: {e}")

@Client.on_callback_query(filters.regex("start"))
async def back_start(client: Client, callback_query):
    try:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("➕ Add Me", url=f"https://t.me/{(await client.get_me()).username}?startgroup=new"),
                InlineKeyboardButton("📚 Commands", callback_data="help")
            ],
            [
                InlineKeyboardButton("💬 Support", url="https://t.me/softxvibessupport"),
                InlineKeyboardButton("📢 Updates", url="https://t.me/softxvibesupdates")
            ]
        ])
        await callback_query.edit_message_text(Messages.START_MESSAGE, reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error: {e}")