import logging
from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.MONGO_DB_URI)
        self.db = self.client['softx_vibes']
        self.users = self.db['users']
        self.chats = self.db['chats']
        self.playlists = self.db['playlists']
        self.settings = self.db['settings']
        self.banned_users = self.db['banned_users']
        self.blacklist_chats = self.db['blacklist_chats']
        self.admins = self.db['admins']
        self.queue = self.db['queue']

    async def add_user(self, user_id, username):
        try:
            if not await self.users.find_one({"_id": user_id}):
                await self.users.insert_one({
                    "_id": user_id,
                    "username": username,
                    "authorized": False,
                    "banned": False,
                    "playtime": 0
                })
        except Exception as e:
            logger.error(f"Error adding user: {e}")

    async def add_chat(self, chat_id, chat_name):
        try:
            if not await self.chats.find_one({"_id": chat_id}):
                await self.chats.insert_one({
                    "_id": chat_id,
                    "name": chat_name,
                    "blacklisted": False,
                    "autoplay": True,
                    "loop_mode": False
                })
        except Exception as e:
            logger.error(f"Error adding chat: {e}")

    async def ban_user(self, user_id, reason=""):
        try:
            await self.banned_users.insert_one({"_id": user_id, "reason": reason})
            await self.users.update_one({"_id": user_id}, {"$set": {"banned": True}})
        except Exception as e:
            logger.error(f"Error banning user: {e}")

    async def unban_user(self, user_id):
        try:
            await self.banned_users.delete_one({"_id": user_id})
            await self.users.update_one({"_id": user_id}, {"$set": {"banned": False}})
        except Exception as e:
            logger.error(f"Error unbanning user: {e}")

    async def is_banned(self, user_id):
        return await self.banned_users.find_one({"_id": user_id}) is not None

    async def authorize_user(self, user_id):
        try:
            await self.users.update_one({"_id": user_id}, {"$set": {"authorized": True}})
        except Exception as e:
            logger.error(f"Error authorizing user: {e}")

    async def unauthorize_user(self, user_id):
        try:
            await self.users.update_one({"_id": user_id}, {"$set": {"authorized": False}})
        except Exception as e:
            logger.error(f"Error unauthorizing user: {e}")

    async def get_authorized_users(self):
        return await self.users.find({"authorized": True}).to_list(None)

    async def get_all_users(self):
        return await self.users.find().to_list(None)

    async def get_all_chats(self):
        return await self.chats.find().to_list(None)

    async def add_playlist(self, user_id, playlist_name, songs):
        try:
            await self.playlists.insert_one({
                "user_id": user_id,
                "name": playlist_name,
                "songs": songs,
                "created_at": None
            })
        except Exception as e:
            logger.error(f"Error adding playlist: {e}")

    async def get_stats(self):
        try:
            users_count = await self.users.count_documents({})
            chats_count = await self.chats.count_documents({})
            banned_users = await self.banned_users.count_documents({})
            blacklist_chats = await self.blacklist_chats.count_documents({})
            return {
                "users": users_count,
                "chats": chats_count,
                "banned_users": banned_users,
                "blacklist_chats": blacklist_chats
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return None

db = MongoDB()

async def init_db():
    logger.info("📊 MongoDB Connected Successfully!")
