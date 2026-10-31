from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@app.on_message(filters.command("start"))
async def start(client, message):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📢 Join Channel",
                    url="https://t.me/YourChannel"
                )
            ]
        ]
    )

    await message.reply_text(
        text="👋 Welcome to TMBot!\n\nPlease join our channel.",
        reply_markup=buttons
    )
