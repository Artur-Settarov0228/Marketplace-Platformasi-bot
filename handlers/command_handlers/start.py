import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.error import NetworkError

from handlers.buttons.auth_buttons import register_button
from utils.config import settings


def start_bot(update: Update, context: CallbackContext):
    telegram_id = update.effective_user.id

    try:
        response = requests.get(
            url=f"{settings.BASE_URL}/api/v1/auth/register/",
            params={"telegram_id": telegram_id},
            timeout=5
        )

        if response.status_code != 200:
            update.message.reply_html(
                "⚠️ <b>Server javob bermadi</b>\n\n"
                "Iltimos, birozdan so‘ng qayta urinib ko‘ring."
            )
            return

        data = response.json()

        # ✅ User mavjud
        if data.get("status"):
            update.message.reply_html(
                "🎉 <b>Xush kelibsiz!</b>\n\n"
                "🔐 Hisobingiz faol.\n"
                "Davom etish uchun: <b>/login</b>"
            )

        # 🆕 User mavjud emas
        else:
            update.message.reply_html(
                "📝 <b>Ro‘yxatdan o‘tish</b>\n\n"
                "Marketplace’dan foydalanish uchun ro‘yxatdan o‘ting 👇",
                reply_markup=register_button()
            )

    except requests.exceptions.Timeout:
        update.message.reply_html(
            "⏳ <b>Server javob bermadi</b>\n\n"
            "Iltimos, internetni tekshirib qayta urinib ko‘ring."
        )

    except requests.exceptions.ConnectionError:
        update.message.reply_html(
            "🔌 <b>Server bilan aloqa uzildi</b>\n\n"
            "Hozircha xizmat mavjud emas.\n"
            "Iltimos keyinroq urinib ko‘ring."
        )

    except requests.exceptions.RequestException as e:
        print("Backend error:", e)

        keyboard = [
            [InlineKeyboardButton("🔄 Qayta urinib ko‘rish", callback_data="retry_start")]
        ]

        update.message.reply_html(
            "⚠️ <b>Kutilmagan xatolik yuz berdi</b>\n\n"
            "Iltimos qayta urinib ko‘ring 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    except NetworkError as e:
        print("Telegram network error:", e)