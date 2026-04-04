import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

app = Flask(__name__)

users = set()

APK_CAPTION = """✅ 100% NUMBER HACK 💥

( ONLY FOR PREMIUM USERS ⚡️ )
( 100% LOSS RECOVER GUARANTEE ⚡️ )

𝐇𝐎𝐖 𝐓𝐎 𝐔𝐒𝐄 :- https://t.me/HOW_TO_USE_JAMES_HACK/6

FOR HELP @M4JAMES_HACK_MANAGER
"""

APK_LINK = "https://raw.githubusercontent.com/loda26616-a11y/JAMES-/1db4bc6a4a7b78311162a7c798e49147eaa4a3e7/JAMES%20INJECTION%20HACK_1.0_0%20(1).apk"

# ✅ BOT INIT
application = ApplicationBuilder().token(BOT_TOKEN).build()


# ✅ JOIN REQUEST
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
            caption=APK_CAPTION
        )

    except Exception as e:
        print("Join Error:", e)


# ✅ BROADCAST
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
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

    except Exception as e:
        print("Broadcast main error:", e)


# ✅ HANDLERS
application.add_handler(ChatJoinRequestHandler(approve_request))
application.add_handler(MessageHandler(filters.ALL, broadcast))


# ✅ WEBHOOK ROUTE
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok"


# ✅ START APP
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    print("Bot running on port", PORT)
    app.run(host="0.0.0.0", port=PORT)
