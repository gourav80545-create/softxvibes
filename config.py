import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram API
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    STRING_SESSION = os.getenv("STRING_SESSION", "")
    
    # Database
    MONGO_DB_URI = os.getenv("MONGO_DB_URI", "")
    
    # Owner & Logging
    OWNER_ID = int(os.getenv("OWNER_ID", "0"))
    LOGGER_ID = int(os.getenv("LOGGER_ID", "0"))
    
    # Support
    SUPPORT_CHAT = int(os.getenv("SUPPORT_CHAT", "0"))
    SUPPORT_CHANNEL = int(os.getenv("SUPPORT_CHANNEL", "0"))
    
    # Bot Settings
    BOT_NAME = os.getenv("BOT_NAME", "Soft X Vibes Music")
    PREFIX = os.getenv("PREFIX", "/")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Features
    OWNER_NAME = "Gourav"
    DEVELOPER_CREDIT = "⚡ MADE BY : 𓆩Gourav𓆪"
    THUMBNAIL_URL = "https://te.legra.ph/file/random.jpg"
    
    # YouTube Cookies (Optional)
    YOUTUBE_COOKIES = os.getenv("YOUTUBE_COOKIES", "")
    
    # Streaming Quality
    QUALITY = "high"
    AUDIO_QUALITY = "high"

class Messages:
    START_MESSAGE = """╔════════════════╗
✨ Welcome To Soft X Vibes Music ✨
╚════════════════╝

🎵 Advanced Voice Chat Music Bot

✨ Features:

• High Quality Music
• Video Streaming
• AutoPlay
• Queue System
• Playlist Support
• Fast Performance
• Beautiful UI
• Admin Controls
• Lyrics Support
• Speed Control

📝 Available Commands:

/play - Play Music
/vplay - Play Video
/pause - Pause Music
/resume - Resume Music
/skip - Skip Song
/stop - Stop Music
/queue - View Queue
/shuffle - Shuffle Queue
/seek - Seek Position
/loop - Loop Mode
/speed - Change Speed
/song - Current Song Info
/lyrics - Get Lyrics
/playlist - Create Playlist
/auth - Authorize User
/unauth - Unauthorize User
/gban - Global Ban User
/broadcast - Send Message
/ping - Check Bot Status
/stats - Bot Statistics

➜ Add me to your group and promote me as Admin."""
    
    HELP_MESSAGE = """🎛 **HELP MENU**

Select a category:"""

class HelpTexts:
    ADMIN = """👮 **ADMIN FEATURES**

/addadmin - Add Admin
/rmadmin - Remove Admin  
/adminlist - Show Admin List
/reloadmin - Reload Admins

Only Owner can use these commands!"""
    
    AUTH = """🔐 **AUTH FEATURES**

/auth <user_id> - Authorize User
/unauth <user_id> - Unauthorize User
/authusers - Show Authorized Users

Only Owner can use these commands!"""
    
    BROADCAST = """📢 **BROADCAST**

/broadcast - Broadcast to Users (reply to message)
/bcgroup - Broadcast to Groups (reply to message)

Only Owner can use these commands!"""
    
    MUSIC = """🎵 **MUSIC COMMANDS**

/play <song> - Play Music
/vplay <video> - Play Video
/pause - Pause Music
/resume - Resume Music
/skip - Skip Song
/stop - Stop Music
/queue - View Queue
/shuffle - Shuffle Queue
/seek <seconds> - Seek Position
/loop - Toggle Loop
/speed <0.5-2.0> - Change Speed
/song - Current Song Info
/lyrics <song> - Get Lyrics
/playlist - Manage Playlists"""
    
    MODERATION = """🚫 **MODERATION**

/gban <user_id> - Global Ban User
/ungban <user_id> - Unban User
/bluser <user_id> - Blacklist User
/blchat <chat_id> - Blacklist Chat

Only Owner can use these commands!"""
    
    MANAGEMENT = """⚙️ **BOT MANAGEMENT**

/ping - Check Bot Status
/stats - Bot Statistics
/logs - View Logs
/restart - Restart Bot
/maintenance - Toggle Maintenance

Most commands only for Owner!"""
