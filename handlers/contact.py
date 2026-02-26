from services.api_client import telegram_login
from services.token_storage import save_token


def handle_contact(update, context):
    user = update.effective_user
    contact = update.message.contact

    # Faqat o‘z contactini yuborganini tekshiramiz
    if contact.user_id != user.id:
        update.message.reply_text("Faqat o'zingizning raqamingizni yuboring ❗")
        return

    payload = {
        "telegram_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": contact.phone_number,
    }

    data = telegram_login(payload)

    if data:
        save_token(user.id, data["access"])
        update.message.reply_text("Registratsiya muvaffaqiyatli ✅")
    else:
        update.message.reply_text("Xatolik yuz berdi ❌")