import logging
import sys
from pyrogram import Client, idle
from config import Config
from database import db
import start, music, admin, auth, moderation, broadcast, management, callbacks

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = Client(
    name="SoftXVibesBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
)

def main():
    try:
        app.start()
        logger.info("⚡ Soft X Vibes Music Bot Started Successfully!")
        
        me = app.get_me()
        logger.info(f"✨ Bot Running as: @{me.username}")
        
        try:
            app.send_message(Config.LOGGER_ID, "⚡ **Soft X Vibes Music Bot Started**\n\n✨ Bot is Online and Ready!")
        except:
            pass
        
        logger.info("📊 Bot initialization completed!")
        idle()
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
