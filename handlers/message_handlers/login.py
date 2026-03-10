import random
import redis
from telegram import Update
from telegram.ext import CallbackContext

# Redis connection
r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    db=0,
    decode_responses=True
)



def generate_otp() -> str:
    """6 xonali OTP generatsiya."""
    return f"{random.randint(100000, 999999)}"


def login_page(update: Update, context: CallbackContext):
    """
    Telegram login flow (production-ready pattern)

    Redis structure:
        login_code:{code} -> telegram_id (TTL 120)
        login_user:{telegram_id} -> code (TTL 120)
    """

    telegram_id = str(update.effective_user.id)
    user_key = f"login_user:{telegram_id}"

    #  Avval mavjud OTP borligini tekshiramiz
    existing_code = r.get(user_key)

    if existing_code:
        ttl = r.ttl(user_key)

        update.message.reply_html(
            "🔐 <b>Avvalgi kod hali amal qiladi</b>\n\n"
            f"⏳ Qolgan vaqt: {ttl} sekund\n"
            f"🔢 Kod: <code>{existing_code}</code>"
        )
        return

    #  Yangi OTP generatsiya
    new_code = generate_otp()

    code_key = f"login_code:{new_code}"

    #  Redis'ga saqlash (atomic tarzda)
    pipe = r.pipeline()
    pipe.setex(code_key, 120, telegram_id)
    pipe.setex(user_key, 120, new_code)
    pipe.execute()

    update.message.reply_html(
        "🔐 <b>Login kodi yaratildi</b>\n\n"
        "⏳ Kod 2 daqiqa amal qiladi.\n\n"
        f"🔢 Kod: <code>{new_code}</code>\n\n"
        "Iltimos, ushbu kodni saytga kiriting."
    )