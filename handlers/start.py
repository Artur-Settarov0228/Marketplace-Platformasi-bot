import requests
from telegram import Update
from telegram.ext import ContextTypes

API_URL = "http://127.0.0.1:8000/api/v1/auth/telegram-login/"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    payload = {
        "telegram_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        data = response.json()
        context.user_data["access_token"] = data["access"]

        await update.message.reply_text("Tizimga kirdingiz ✅")
    elif response.status_code == 400:
        await update.message.reply_text("Ro'yxatdan o'tish uchun raqamingizni yuboring 📱")
    else:
        await update.message.reply_text("Xatolik ❌")