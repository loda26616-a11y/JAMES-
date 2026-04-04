import os
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

users = set()

APK_CAPTION = """
✅ 100% NUMBER HACK 💥

( ONLY FOR PREMIUM USERS ⚡️ )
( 100% LOSS RECOVER GUARANTEE ⚡️ )

𝐇𝐎𝐖 𝐓𝐎 𝐔𝐒𝐄 𝐇𝐀𝐂𝐊 :- https://t.me/HOW_TO_USE_JAMES_HACK/6

FOR HELP @M4JAMES_HACK_MANAGER
"""


# ✅ Join Request Auto Approve
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.chat_join_request.from_user
        chat_id = update.chat_join_request.chat.id

        # approve join request
        await context.bot.approve_chat_join_request(chat_id, user.id)

        users.add(user.id)

        # send welcome message in DM
        await context.bot.send_message(
            chat_id=user.id,
            text="✨ WELCOME TO JAMES PREMIUM BOT ✨\n\nAccess Granted 🚀"
        )

        # send APK
        with open("app.apk", "rb") as apk:
            await context.bot.send_document(
                chat_id=user.id,
                document=apk,
                caption=APK_CAPTION
            )

    except Exception as e:
        print(f"Error in approve_request: {e}")


# ✅ Broadcast message (only admin)
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
                print(f"Broadcast error to {user_id}: {e}")

    except Exception as e:
        print(f"Broadcast main error: {e}")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(ChatJoinRequestHandler(approve_request))
    app.add_handler(MessageHandler(filters.ALL, broadcast))

    print("✅ Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
