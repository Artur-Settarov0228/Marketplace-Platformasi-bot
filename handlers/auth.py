import httpx
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from config import API_URL, API_KEY


def contact_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "Tizimga kirish uchun telefon raqamingizni yuboring 👇",
        reply_markup=contact_keyboard()
    )


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    async with httpx.AsyncClient() as client:
        response = await client.post(
            API_URL,
            json={"telegram_id": telegram_id},
            headers={"X-API-KEY": API_KEY}
        )

    data = response.json()

    await update.message.reply_text(
        f"🔐 Login kodi: {data['code']}\n"
        "⏳ 1 daqiqa amal qiladi.\n"
        "Saytga qaytib kodni kiriting.",
        reply_markup=ReplyKeyboardRemove()
    )


async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_contact(update, context)