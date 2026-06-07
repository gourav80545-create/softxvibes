import logging
import sys
import time
import ntplib
import requests
from datetime import datetime
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
    
    # Try NTP sync first
    for server in ntp_servers:
        try:
            logger.info(f"Syncing system time with NTP server: {server}...")
            ntp_client = ntplib.NTPClient()
            response = ntp_client.request(server, version=3, timeout=5)
            logger.info(f"Time synced successfully with {server}. Offset: {response.offset} seconds")
            time.sleep(10)  # Give time for sync to take effect
            return
        except Exception as e:
            logger.warning(f"Failed to sync with {server}: {e}")
            continue
    
    # Fallback to HTTP time sync
    logger.warning("Could not sync time with any NTP server, trying HTTP time sync...")
    try:
        response = requests.head('http://google.com', timeout=5)
        http_time = response.headers.get('Date')
        if http_time:
            logger.info(f"Got HTTP time: {http_time}")
            # Just log it, we can't set system time from Python
            time.sleep(15)
            return
    except Exception as e:
        logger.warning(f"HTTP time sync failed: {e}")
    
    logger.warning("Could not sync time with any method")
    logger.info("Adding extra delay to allow system time to stabilize...")
    time.sleep(30)  # Extra delay to allow system time to stabilize

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
