import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    STRING_SESSION = os.getenv("STRING_SESSION", "")
    MONGO_DB_URI = os.getenv("MONGO_DB_URI", "")
    OWNER_ID = int(os.getenv("OWNER_ID", "0"))
    LOGGER_ID = int(os.getenv("LOGGER_ID", "0"))
    SUPPORT_CHAT = int(os.getenv("SUPPORT_CHAT", "0"))
    SUPPORT_CHANNEL = int(os.getenv("SUPPORT_CHANNEL", "0"))
    
    BOT_NAME = "Soft X Vibes Music"
    OWNER_NAME = "Gourav"
    DEVELOPER_CREDIT = "⚡ MADE BY : 𓆩Gourav𓆪"

class Messages:
    START_MESSAGE = """╔════════════════╗
✨ Welcome To Soft X Vibes Music ✨
╚════════════════╝

🎵 Advanced Voice Chat Music Bot

📝 Available Commands:
/play, /vplay, /pause, /resume, /skip, /stop, /queue, /shuffle, /seek, /loop, /speed, /song, /lyrics, /playlist

➜ Add me to your group and promote me as Admin."""

    HELP_MESSAGE = "🎛 **HELP MENU**\n\nSelect a category:"

class HelpTexts:
    ADMIN = "👮 Admin commands here..."
    AUTH = "🔐 Auth commands here..."
    MUSIC = "🎵 Music commands here..."
