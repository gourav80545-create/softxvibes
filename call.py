import asyncio
from typing import Optional

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.exceptions import NoActiveGroupCall

from config import Config
from client import app

class Call:
    def __init__(self):
        self.userbot1 = Client(
            "SoftXVibesAssis1", 
            Config.API_ID, 
            Config.API_HASH, 
            session_string=Config.STRING1
        ) if Config.STRING1 else None
        self.one = PyTgCalls(self.userbot1) if self.userbot1 else None

        self.userbot2 = Client(
            "SoftXVibesAssis2", 
            Config.API_ID, 
            Config.API_HASH, 
            session_string=Config.STRING2
        ) if Config.STRING2 else None
        self.two = PyTgCalls(self.userbot2) if self.userbot2 else None

        self.userbot3 = Client(
            "SoftXVibesAssis3", 
            Config.API_ID, 
            Config.API_HASH, 
            session_string=Config.STRING3
        ) if Config.STRING3 else None
        self.three = PyTgCalls(self.userbot3) if self.userbot3 else None

        self.userbot4 = Client(
            "SoftXVibesAssis4", 
            Config.API_ID, 
            Config.API_HASH, 
            session_string=Config.STRING4
        ) if Config.STRING4 else None
        self.four = PyTgCalls(self.userbot4) if self.userbot4 else None

        self.userbot5 = Client(
            "SoftXVibesAssis5", 
            Config.API_ID, 
            Config.API_HASH, 
            session_string=Config.STRING5
        ) if Config.STRING5 else None
        self.five = PyTgCalls(self.userbot5) if self.userbot5 else None

        self.active_calls: set[int] = set()
        self.assistants = []
        
        # Initialize available assistants
        if self.one:
            self.assistants.append(self.one)
        if self.two:
            self.assistants.append(self.two)
        if self.three:
            self.assistants.append(self.three)
        if self.four:
            self.assistants.append(self.four)
        if self.five:
            self.assistants.append(self.five)

    async def start_assistants(self):
        """Start all assistant userbots"""
        for i, assistant in enumerate([self.userbot1, self.userbot2, self.userbot3, self.userbot4, self.userbot5]):
            if assistant:
                try:
                    await assistant.start()
                    print(f"✅ Assistant {i+1} started")
                except Exception as e:
                    print(f"❌ Assistant {i+1} failed to start: {e}")
        
        # Start PyTgCalls instances
        for i, pytg in enumerate([self.one, self.two, self.three, self.four, self.five]):
            if pytg:
                try:
                    await pytg.start()
                    print(f"✅ PyTgCalls {i+1} started")
                except Exception as e:
                    print(f"❌ PyTgCalls {i+1} failed to start: {e}")

    async def stop_assistants(self):
        """Stop all assistant userbots"""
        for i, assistant in enumerate([self.userbot1, self.userbot2, self.userbot3, self.userbot4, self.userbot5]):
            if assistant:
                try:
                    await assistant.stop()
                    print(f"✅ Assistant {i+1} stopped")
                except Exception as e:
                    print(f"❌ Assistant {i+1} failed to stop: {e}")
        
        # Stop PyTgCalls instances
        for i, pytg in enumerate([self.one, self.two, self.three, self.four, self.five]):
            if pytg:
                try:
                    await pytg.stop()
                    print(f"✅ PyTgCalls {i+1} stopped")
                except Exception as e:
                    print(f"❌ PyTgCalls {i+1} failed to stop: {e}")

    def get_assistant(self, chat_id: int) -> Optional[PyTgCalls]:
        """Get an available assistant for the chat"""
        if not self.assistants:
            return None
        # Simple round-robin selection
        index = chat_id % len(self.assistants)
        return self.assistants[index]

    async def join_voice_chat(self, chat_id: int):
        """Join a voice chat"""
        assistant = self.get_assistant(chat_id)
        if not assistant:
            raise Exception("No assistant available")
        
        try:
            await assistant.join_group_call(chat_id)
            self.active_calls.add(chat_id)
            print(f"✅ Joined voice chat {chat_id}")
        except NoActiveGroupCall:
            raise Exception("No active voice chat in this group")
        except Exception as e:
            raise Exception(f"Failed to join voice chat: {e}")

    async def leave_voice_chat(self, chat_id: int):
        """Leave a voice chat"""
        assistant = self.get_assistant(chat_id)
        if not assistant:
            return
        
        try:
            await assistant.leave_group_call(chat_id)
            self.active_calls.discard(chat_id)
            print(f"✅ Left voice chat {chat_id}")
        except Exception as e:
            print(f"❌ Failed to leave voice chat: {e}")

# Global call instance
call = Call()
