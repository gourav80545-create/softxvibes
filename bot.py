import logging
import sys
import time
import ntplib
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
    "SoftXVibesBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
)

def sync_time():
    """Sync system time using NTP to avoid Pyrogram time sync errors"""
    ntp_servers = [
        'pool.ntp.org',
        'time.google.com',
        'time.cloudflare.com',
        'time.nist.gov'
    ]
    
    for server in ntp_servers:
        try:
            logger.info(f"Syncing system time with NTP server: {server}...")
            ntp_client = ntplib.NTPClient()
            response = ntp_client.request(server, version=3, timeout=5)
            logger.info(f"Time synced successfully with {server}. Offset: {response.offset} seconds")
            time.sleep(5)  # Give time for sync to take effect
            return
        except Exception as e:
            logger.warning(f"Failed to sync with {server}: {e}")
            continue
    
    logger.warning("Could not sync time with any NTP server")
    logger.info("Adding extra delay to allow system time to stabilize...")
    time.sleep(10)  # Extra delay to allow system time to stabilize

def main():
    try:
        # Sync time before starting bot to avoid Pyrogram time sync errors
        sync_time()
        
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
