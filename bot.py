from pyrogram import Client, filters

from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "MangaBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


@app.on_message(filters.command("start"))
async def start(client, message):

    await message.reply_text(
        "Welcome to MangaBot!"
    )


app.run()
