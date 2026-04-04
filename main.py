from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatJoinRequestHandler
from telegram.error import NetworkError, TimedOut, RetryAfter
import json
import os
import asyncio
import requests
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
APK_URL = os.environ.get("APK_URL")

USERS_FILE = "telegram-bot/users.json"

DM_LINK = "https://t.me/M4JAMES_HACK_MANAGER?text=HELLO%20JAMES%20BHAI%20MUJHE%20LOSS%20RECOVER%20KRWANA%20HAI"
VIP_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("VIP CHANNEL LINK ❤️✨", url=DM_LINK)]
])


def load_users():
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return []


def save_users(users):
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)
    except IOError as e:
        print(f"Error saving users: {e}")


def add_user(user, users):
    if not any(u["id"] == user.id for u in users):
        users.append({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "joined_at": datetime.now().isoformat()
        })
        save_users(users)
    return users


def download_apk():
    if not APK_URL:
        print("APK_URL not set, skipping APK send.")
        return None
    try:
        print(f"Downloading APK from GitHub...")
        response = requests.get(APK_URL, timeout=60)
        response.raise_for_status()
        print(f"APK downloaded successfully ({len(response.content)} bytes)")
        return response.content
    except Exception as e:
        print(f"Failed to download APK: {e}")
        return None


async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat_id = update.chat_join_request.chat.id

    for attempt in range(3):
        try:
            await context.bot.approve_chat_join_request(chat_id, user.id)

            users = load_users()
            add_user(user, users)

            await context.bot.send_message(
                chat_id=user.id,
                text="🚀🔥 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗝𝗔𝗠𝗘𝗦 𝗧𝗥𝗔𝗗𝗘𝗥𝗦 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗕𝗢𝗧 🔥",
                reply_markup=VIP_BUTTON
            )

            if APK_URL:
                apk_data = download_apk()
                if apk_data:
                    from io import BytesIO
                    apk_file = BytesIO(apk_data)
                    apk_file.name = "JAMES PREMIUM INJECTOR HACK.apk"
                    await context.bot.send_document(
                        chat_id=user.id,
                        document=apk_file,
                        filename="JAMES PREMIUM INJECTOR HACK.apk",
                        caption=(
                            "✅ 100% NUMBER HACK 💥\n\n"
                            "( ONLY FOR PREMIUM USERS ⚡️ )\n"
                            "( 100% LOSS RECOVER GUARANTEE ⚡️ )\n\n"
                            "𝐇𝐎𝐖 𝐓𝐎 𝐔𝐒𝐄 𝐇𝐀𝐂𝐊 :- https://t.me/HOW_TO_USE_JAMES_HACK/6\n"
                            "FOR HELP @M4JAMES_HACK_MANAGER"
                        ),
                        reply_markup=VIP_BUTTON
                    )

            print(f"[{datetime.now()}] Approved user: {user.id} (@{user.username})")
            break

        except RetryAfter as e:
            print(f"Rate limited, waiting {e.retry_after} seconds...")
            await asyncio.sleep(e.retry_after)
        except (NetworkError, TimedOut) as e:
            print(f"Network error (attempt {attempt + 1}/3): {e}")
            if attempt < 2:
                await asyncio.sleep(5)
        except Exception as e:
            print(f"Error handling join request: {e}")
            break


def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN environment variable not set")
        import time
        time.sleep(30)
        return

    print(f"[{datetime.now()}] Bot starting...")
    if APK_URL:
        print(f"[{datetime.now()}] APK URL configured: {APK_URL[:50]}...")
    else:
        print(f"[{datetime.now()}] WARNING: APK_URL not set, APK will not be sent.")

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .get_updates_pool_timeout(30)
        .get_updates_read_timeout(30)
        .get_updates_write_timeout(30)
        .get_updates_connect_timeout(30)
        .build()
    )

    app.add_handler(ChatJoinRequestHandler(join_request))

    print(f"[{datetime.now()}] Bot running - waiting for join requests...")

    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=["chat_join_request"]
    )


if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Bot stopped by user")
            break
        except Exception as e:
            print(f"[{datetime.now()}] Bot crashed: {e}")
            print("Restarting in 10 seconds...")
            import time
            time.sleep(10)
