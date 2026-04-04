import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from flask import Flask, request
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

APK_LINK = "https://raw.githubusercontent.com/loda26616-a11y/JAMES-/1db4bc6a4a7b78311162a7c798e49147eaa4a3e7/JAMES%20INJECTION%20HACK_1.0_0%20(1).apk"

users = set()

flask_app = Flask(__name__)
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()


# ✅ Handlers
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.chat_join_request.from_user
        chat_id = update.chat_join_request.chat.id

        await context.bot.approve_chat_join_request(chat_id, user.id)
        users.add(user.id)

        await context.bot.send_message(
            chat_id=user.id,
            text="✨ WELCOME TO JAMES PREMIUM BOT ✨\n\nAccess Granted 🚀"
        )

        await context.bot.send_document(
            chat_id=user.id,
            document=APK_LINK,
            caption="✅ APK FILE"
        )

    except Exception as e:
        print("Approve error:", e)


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    for user_id in users:
        try:
            await context.bot.copy_message(
                chat_id=user_id,
                from_chat_id=update.effective_chat.id,
                message_id=update.message.id
            )
        except Exception as e:
            print("Broadcast error:", e)


telegram_app.add_handler(ChatJoinRequestHandler(approve_request))
telegram_app.add_handler(MessageHandler(filters.ALL, broadcast))


# ✅ Webhook route
@flask_app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, telegram_app.bot)

        asyncio.run(telegram_app.process_update(update))
        return "ok"
    except Exception as e:
        print("Webhook error:", e)
        return "error"


# ✅ Home route
@flask_app.route("/")
def home():
    return "Bot Running 🚀"


# 🔥 IMPORTANT STARTUP
async def start_bot():
    await telegram_app.initialize()
    await telegram_app.start()

asyncio.run(start_bot())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)
