import random
import redis
from telegram import Update
from telegram.ext import CallbackContext

# Redis connection (production'da settings orqali beriladi)
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)


def login_page(update: Update, context: CallbackContext):
    """
    Telegram login sahifasi.

    Flow:
        1. Foydalanuvchi /login bosadi.
        2. Agar mavjud OTP hali tugamagan bo‘lsa — o‘sha kod qayta ko‘rsatiladi.
        3. Agar mavjud bo‘lmasa — yangi 6 xonali OTP yaratiladi.
        4. OTP Redis’da 2 daqiqa (120s) saqlanadi.
    
    Redis key structure:
        login_code:{telegram_id} -> OTP

    Security:
        - OTP user bilan bog‘langan (code orqali user topilmaydi)
        - TTL mavjud
    """

    telegram_id = update.effective_user.id
    redis_key = f"login_code:{telegram_id}"

    # Mavjud OTP ni tekshirish
    existing_code = r.get(redis_key)

    if existing_code:
        update.message.reply_html(
            "🔐 <b>Avvalgi kod hali amal qiladi</b>\n\n"
            f"⏳ Amal qilish muddati: 2 daqiqa\n"
            f"🔢 Kod: <code>{existing_code}</code>"
        )
        return

    # Yangi OTP generatsiya
    new_code = str(random.randint(100000, 999999))

    # Redis’da saqlash (120 sekund)
    r.setex(redis_key, 120, new_code)

    update.message.reply_html(
        "🔐 <b>Login kodi yaratildi</b>\n\n"
        "⏳ Kod 2 daqiqa amal qiladi.\n\n"
        f"🔢 Kod: <code>{new_code}</code>\n\n"
        "Iltimos, ushbu kodni saytga kiriting."
    )