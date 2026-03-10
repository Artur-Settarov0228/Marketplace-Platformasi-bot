import requests

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler

from utils.config import RegisterStep, settings
from handlers.buttons.auth_buttons import send_contact, confirm_button



def register_handler(update: Update, context: CallbackContext):
    """
    Registration boshlanish bosqichi.
    Foydalanuvchidan ism va familiya so‘raladi.
    """
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        "📝 <b>Ro‘yxatdan o‘tish</b>\n\n"
        "Iltimos, <b>ism</b> va <b>familiyangizni</b> kiriting.\n"
        "Masalan: <code>Ali Valiyev</code>",
        parse_mode="HTML"
    )

    return RegisterStep.FULL_NAME



def get_full_name(update: Update, context: CallbackContext):
    """
    Foydalanuvchidan ism va familiyani qabul qiladi.
    """
    text = update.message.text.strip()
    parts = text.split()

    if len(parts) < 2:
        update.message.reply_html(
            "❗ <b>Xatolik</b>\n\n"
            "Iltimos ism va familiyangizni to‘liq kiriting.\n"
            "Masalan: <code>Ali Valiyev</code>"
        )
        return RegisterStep.FULL_NAME

    context.user_data['first_name'] = parts[0].title()
    context.user_data['last_name'] = parts[1].title()

    update.message.reply_html(
        "📱 <b>Telefon raqam</b>\n\n"
        "Quyidagi tugma orqali kontaktingizni yuboring 👇",
        reply_markup=send_contact()
    )

    return RegisterStep.PHONE_NUMBER



def get_phone_number(update: Update, context: CallbackContext):
    """
    Telefon raqamni qabul qiladi.
    """
    if not update.message.contact:
        update.message.reply_text("❗ Iltimos tugma orqali kontakt yuboring.")
        return RegisterStep.PHONE_NUMBER

    context.user_data['contact'] = update.message.contact.phone_number

    update.message.reply_html(
        " <b>Profile rasmi</b>\n\n"
        "Profilingiz uchun rasm yuboring iltimos.",
        reply_markup=ReplyKeyboardRemove()
    )

    return RegisterStep.AVATAR



def get_avatar_image(update: Update, context: CallbackContext):
    """
    Avatar qabul qiladi va tasdiqlash sahifasini ko‘rsatadi.
    """

    if not update.message.photo:
        update.message.reply_text("❗ Iltimos rasm yuboring.")
        return RegisterStep.AVATAR

    file_id = update.message.photo[-1].file_id
    context.user_data['file_id'] = file_id

    caption = (
        "📋 <b>Ma'lumotlaringizni tasdiqlang</b>\n\n"
        f"👤 <b>Ism:</b> {context.user_data['first_name']}\n"
        f"👤 <b>Familiya:</b> {context.user_data['last_name']}\n"
        f"📱 <b>Telefon:</b> {context.user_data['contact']}\n\n"
        "Ma'lumotlar to‘g‘rimi?"
    )

    update.message.reply_photo(
        photo=file_id,
        caption=caption,
        reply_markup=confirm_button(),
        parse_mode="HTML"
    )

    return RegisterStep.CONFIRM



def confirm_data(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    print("CALLBACK:", query.data)

    if query.data == "register:confirm":

        data = {
            "telegram_id": update.effective_user.id,
            "username": update.effective_user.username,
            "first_name": context.user_data['first_name'],
            "last_name": context.user_data['last_name'],
            "phone_number": context.user_data['contact'],
            "avatar": context.user_data['file_id']
        }

        response = requests.post(
            f"{settings.BASE_URL}/api/v1/auth/register/",
            json=data,
            timeout=5
        )

        if response.status_code == 201:
            query.edit_message_caption(
                caption="✅ Ro‘yxatdan o‘tish muvaffaqiyatli 🎉",
                parse_mode="HTML"
            )
            context.user_data.clear()
            return ConversationHandler.END

        else:
            query.edit_message_caption(
                caption=f"❌ Server error: {response.text}",
                parse_mode="HTML"
            )
            return RegisterStep.CONFIRM

    elif query.data == "register:retry":

        query.edit_message_caption(
            caption="🔁 Iltimos ism va familiyangizni qayta kiriting.",
            parse_mode="HTML"
        )
        return RegisterStep.FULL_NAME