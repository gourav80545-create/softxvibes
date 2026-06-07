import logging
import sys
import time
import ntplib
import requests
from datetime import datetime
from pyrogram import Client, idle
from config import Config
from database import db
from flask import Flask
from threading import Thread
import os

# Import handlers AFTER creating the client
# This ensures decorators register with the correct client instance

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Flask app for Render port binding
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running!"

@flask_app.route('/health')
def health():
    return {"status": "ok"}, 200

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    flask_app.run(host='0.0.0.0', port=port, use_reloader=False, threaded=True)

app = Client(
    "SoftXVibesBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workdir="/tmp",  # Use /tmp for session files
    in_memory=True  # Use in-memory session to avoid file permission issues
)

# Import handlers AFTER creating the client
# This ensures decorators register with the correct client instance
import start, music, admin, auth, moderation, broadcast, management, callbacks

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
        
        # Try to start the bot with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                app.start()
                logger.info("⚡ Soft X Vibes Music Bot Started Successfully!")
                break
            except Exception as e:
                if "msg_id is too low" in str(e):
                    logger.warning(f"Time sync error on attempt {attempt + 1}/{max_retries}, retrying...")
                    time.sleep(30)  # Wait longer before retry
                    if attempt == max_retries - 1:
                        raise
                else:
                    raise
        
        # Start Flask server in a separate thread for Render port binding
        flask_thread = Thread(target=run_flask)
        flask_thread.daemon = True
        flask_thread.start()
        logger.info("Flask server started on port %s", os.environ.get('PORT', 8080))
        
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
