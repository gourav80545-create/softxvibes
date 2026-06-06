import logging
import sys
from pyrogram import Client, idle
from config import Config
from database.mongo_db import init_db
import asyncio

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

async def main():
    try:
        await app.start()
        logger.info("⚡ Soft X Vibes Music Bot Started Successfully!")
        me = await app.get_me()
        logger.info(f"✨ Bot Running as: @{me.username}")
        
        await init_db()
        
        try:
            await app.send_message(Config.LOGGER_ID, "⚡ **Soft X Vibes Music Bot Started**\n\n✨ Bot is Online and Ready!")
        except:
            pass
        
        await idle()
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    finally:
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())