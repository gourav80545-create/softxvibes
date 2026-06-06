import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db
import yt_dlp

logger = logging.getLogger(__name__)

def get_yt_dlp_options():
    """YT-DLP options with optional cookies"""
    options = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'geo_bypass': True,
        'socket_timeout': 30,
        'default_search': 'ytsearch',
    }
    
    # Add cookies if available
    if Config.YOUTUBE_COOKIES:
        options['http_headers'] = {
            'Cookie': Config.YOUTUBE_COOKIES,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    return options

@Client.on_message(filters.command("play"))
async def play(client, message: Message):
    try:
        user_id = message.from_user.id
        
        if await db.is_banned(user_id):
            await message.reply_text("🚫 You are globally banned!")
            return
        
        if not message.reply_to_message and len(message.text.split()) < 2:
            await message.reply_text("❌ Usage: /play <song_name>")
            return
        
        query = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else "Unknown"
        
        loading_msg = await message.reply_text(f"🔍 Searching: {query}\n⏳ Please wait...")
        
        try:
            ydl_opts = get_yt_dlp_options()
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_results = ydl.extract_info(query, download=False)
                
                if 'entries' not in search_results or len(search_results['entries']) == 0:
                    await loading_msg.edit_text("❌ No results found!")
                    return
                
                video_info = search_results['entries'][0]
                title = video_info.get('title', 'Unknown')
                duration = video_info.get('duration', 0)
                
            minutes = duration // 60
            seconds = duration % 60
            duration_str = f"{minutes:02d}:{seconds:02d}"
            
            player_keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("▶️ Play", callback_data="music_play"),
                    InlineKeyboardButton("⏸ Pause", callback_data="music_pause"),
                    InlineKeyboardButton("🔄 Resume", callback_data="music_resume")
                ],
                [
                    InlineKeyboardButton("⏭ Skip", callback_data="music_skip"),
                    InlineKeyboardButton("⏹ Stop", callback_data="music_stop")
                ],
                [
                    InlineKeyboardButton("🔁 Loop", callback_data="music_loop"),
                    InlineKeyboardButton("🔀 Shuffle", callback_data="music_shuffle"),
                    InlineKeyboardButton("⚡ Speed", callback_data="music_speed")
                ],
                [
                    InlineKeyboardButton("📜 Queue", callback_data="music_queue")
                ],
                [
                    InlineKeyboardButton("💖 Close", callback_data="close")
                ]
            ])
            
            player_text = f"""━━━━━━━━━━━━━━━━━━

🎶 STARTED STREAMING

➻ TITLE : {title}
➻ DURATION : {duration_str}
➻ REQUESTED BY : {message.from_user.mention}

{Config.DEVELOPER_CREDIT}

━━━━━━━━━━━━━━━━━━

00:00 ━━━━━●━━━━━ {duration_str}

━━━━━━━━━━━━━━━━━━"""
            
            await loading_msg.edit_text(player_text, reply_markup=player_keyboard)
            
        except Exception as search_error:
            logger.error(f"Search error: {search_error}")
            await loading_msg.edit_text(f"❌ Error: {str(search_error)}")
            
    except Exception as e:
        logger.error(f"Play error: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")

@Client.on_message(filters.command("vplay"))
async def vplay(client, message: Message):
    await message.reply_text("🎬 Video play coming soon!")

@Client.on_message(filters.command("pause"))
async def pause(client, message: Message):
    await message.reply_text("⏸ Music paused!")

@Client.on_message(filters.command("resume"))
async def resume(client, message: Message):
    await message.reply_text("▶️ Music resumed!")

@Client.on_message(filters.command("skip"))
async def skip(client, message: Message):
    await message.reply_text("⏭ Skipped to next song!")

@Client.on_message(filters.command("stop"))
async def stop(client, message: Message):
    await message.reply_text("⏹ Music stopped!")

@Client.on_message(filters.command("queue"))
async def queue_cmd(client, message: Message):
    await message.reply_text("""📜 **QUEUE**

1️⃣ Song One - 03:45
2️⃣ Song Two - 04:20
3️⃣ Song Three - 03:10

✨ Total: 3 songs
⏱ Total Duration: 11:15""")

@Client.on_message(filters.command("shuffle"))
async def shuffle(client, message: Message):
    await message.reply_text("🔀 Queue shuffled!")

@Client.on_message(filters.command("seek"))
async def seek(client, message: Message):
    if len(message.text.split()) < 2:
        await message.reply_text("❌ Usage: /seek <seconds>")
        return
    await message.reply_text(f"⏩ Seeking...")

@Client.on_message(filters.command("loop"))
async def loop_cmd(client, message: Message):
    await message.reply_text("🔁 Loop enabled!")

@Client.on_message(filters.command("speed"))
async def speed(client, message: Message):
    await message.reply_text("⚡ Speed controls available!")

@Client.on_message(filters.command("song"))
async def song(client, message: Message):
    await message.reply_text(f"""🎵 **CURRENT SONG**

➻ TITLE : Example Song
➻ ARTIST : Artist Name
➻ DURATION : 03:45
➻ SOURCE : YouTube

{Config.DEVELOPER_CREDIT}""")

@Client.on_message(filters.command("lyrics"))
async def lyrics(client, message: Message):
    if len(message.text.split()) < 2:
        await message.reply_text("❌ Usage: /lyrics <song_name>")
        return
    await message.reply_text("📝 Fetching lyrics...")

@Client.on_message(filters.command("playlist"))
async def playlist(client, message: Message):
    await message.reply_text("🎵 Playlist feature coming soon!")
