import os
import asyncio
from aiohttp import web
from pyrogram import Client, filters
from pyrogram.types import Message

# Render port
PORT = int(os.environ.get("PORT", 8080))

# Telegram Credentials
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "").strip()
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()

# Print check to verify env variables exist
print(f"DEBUG: API_ID is {'SET' if API_ID else 'EMPTY'}")
print(f"DEBUG: API_HASH is {'SET' if API_HASH else 'EMPTY'}")
print(f"DEBUG: BOT_TOKEN is {'SET' if BOT_TOKEN else 'EMPTY'}")

app = Client(
    name="my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Case-insensitive /start handler + normal text fallback
@app.on_message(filters.command(["start", "Start", "START"]) & filters.private)
async def start_handler(client: Client, message: Message):
    print(f"DEBUG: /start received from {message.from_user.id}")
    await message.reply_text(f"Hi {message.from_user.first_name}! 👋\nBot ekdum theek chal raha hai.")

# Dummy route for Render health check
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def start_web():
    server = web.Application()
    server.router.add_get("/", handle_ping)
    runner = web.AppRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"Web server listening on port {PORT}")

async def main():
    await start_web()
    print("Starting Telegram Bot...")
    await app.start()
    me = await app.get_me()
    print(f"Bot connected as @{me.username} ({me.id})")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
