import os
import asyncio
import aiohttp

from aiohttp import web
from pyrogram import Client, filters
from pyrogram.types import Message

# Render Port
PORT = int(os.environ.get("PORT", 8080))

# Telegram Credentials
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "").strip()
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()

# Channel
CHANNEL_URL = "https://t.me/YourChannel"

print(f"DEBUG: API_ID is {'SET' if API_ID else 'EMPTY'}")
print(f"DEBUG: API_HASH is {'SET' if API_HASH else 'EMPTY'}")
print(f"DEBUG: BOT_TOKEN is {'SET' if BOT_TOKEN else 'EMPTY'}")

app = Client(
    name="my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# START COMMAND
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):

    user = message.from_user

    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "🔵 Join Channel",
                    "url": CHANNEL_URL,
                    "style": "primary"
                }
            ],
            [
                {
                    "text": "🟢 Verify",
                    "callback_data": "verify",
                    "style": "success"
                }
            ],
            [
                {
                    "text": "🔴 Cancel",
                    "callback_data": "cancel",
                    "style": "danger"
                }
            ]
        ]
    }

    async with aiohttp.ClientSession() as session:

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": message.chat.id,
            "text": (
                f"Hi {user.first_name}! 👋\n\n"
                "Bot ekdum theek chal raha hai."
            ),
            "reply_markup": keyboard
        }

        async with session.post(url, json=payload) as response:
            result = await response.json()
            print("DEBUG:", result)


# CALLBACK HANDLER
@app.on_callback_query()
async def callback_handler(client, query):

    if query.data == "verify":
        await query.answer("Verification coming soon!", show_alert=True)

    elif query.data == "cancel":
        await query.message.delete()


# Render Health Check
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


# MAIN
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
