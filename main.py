import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

users = set()

# 👉 Yaha APK caption edit kar sakte ho
APK_CAPTION = "✅ 100% NUMBER HACK 💥

( ONLY FOR PREMIUM USERS ⚡️ )
( 100% LOSS RECOVER GUARANTEE ⚡️ )

𝐇𝐎𝐖 𝐓𝐎 𝐔𝐒𝐄 𝐇𝐀𝐂𝐊 :- https://t.me/HOW_TO_USE_JAMES_HACK/6

FOR HELP @M4JAMES_HACK_MANAGER""
"""

# JOIN REQUEST APPROVE
async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):

    req = update.chat_join_request
    user = req.from_user

    await req.approve()

    users.add(user.id)

    welcome_text = (
        "✨ 𝙒𝙀𝙇𝘾𝙊𝙈𝙀 ✨\n\n"
        "🚀 Welcome To 𝗝𝗔𝗠𝗘𝗦 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗕𝗢𝗧\n\n"
        "🔥 Premium Access Activated\n"
        "📲 Download The App Below 👇"
    )

    try:

        await context.bot.send_message(
            chat_id=user.id,
            text=welcome_text
        )

        with open("app.apk", "rb") as apk:

            await context.bot.send_document(
                chat_id=user.id,
                document=apk,
                caption=APK_CAPTION
            )

    except:
        pass


# BROADCAST
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    for user in users:
        try:
            await update.message.copy(chat_id=user)
        except:
            pass

    await update.message.reply_text("✅ Broadcast Sent")


def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(ChatJoinRequestHandler(join_request))
    app.add_handler(MessageHandler(filters.ALL & filters.User(ADMIN_ID), broadcast))

    print("Bot Running...")

    app.run_polling()


if __name__ == "__main__":
    main()
