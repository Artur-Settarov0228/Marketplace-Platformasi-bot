from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def register_button():
    keyboard = [
        [
            InlineKeyboardButton(
                text="🚀 Ro‘yxatdan o‘tishni boshlash",
                callback_data="register:start"
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def send_contact():
    keyboard = [
        [
            KeyboardButton(
                text="📲 Telefon raqamni yuborish",
                request_contact=True
            )
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Telefon raqamingizni yuboring..."
    )


def confirm_button():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Tasdiqlash", callback_data="register:confirm"),
            InlineKeyboardButton("🔄 Qayta kiritish", callback_data="register:retry")
        ]
    ])
    # return InlineKeyboardMarkup(keyboard)