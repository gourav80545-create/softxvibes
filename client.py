from pyrogram import Client
from config import Config

app = Client(
    "SoftXVibesBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workdir="/tmp",  # Use /tmp for session files
    in_memory=True  # Use in-memory session to avoid file permission issues
)
