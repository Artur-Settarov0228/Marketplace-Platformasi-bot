from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    Filters,
)

from handlers.command_handlers.start import start_bot
from handlers.message_handlers.login import login_page
from handlers.message_handlers.registration import (
    register_handler,
    get_full_name,
    get_phone_number,
    get_avatar_image,
    confirm_data,
)

from utils.config import settings, RegisterStep


def main():
    """
    Botni ishga tushirish funksiyasi.

    Flow:
        /start → mavjud user tekshiriladi
        /login → OTP beriladi
        register:start → ConversationHandler orqali register jarayoni
    """

    # =========================
    # Bot initialization
    # =========================
    updater = Updater(token=settings.TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # =========================
    # Command Handlers
    # =========================
    dispatcher.add_handler(CommandHandler("start", start_bot))
    dispatcher.add_handler(CommandHandler("login", login_page))

    # Inline login tugmasi uchun
    dispatcher.add_handler(
        CallbackQueryHandler(login_page, pattern=r"^login_page$")
    )

    # =========================
    # Registration Conversation
    # =========================
    register_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                register_handler,
                pattern=r"^register:start$"
            )
        ],
        states={
            RegisterStep.FULL_NAME: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    get_full_name
                )
            ],
            RegisterStep.PHONE_NUMBER: [
                MessageHandler(
                    Filters.contact,
                    get_phone_number
                )
            ],
            RegisterStep.AVATAR: [
                MessageHandler(
                    Filters.photo,
                    get_avatar_image
                )
            ],
            RegisterStep.CONFIRM: [
                CallbackQueryHandler(
                    confirm_data,
                    pattern=r"^register:"
                )
            ],
        },
        fallbacks=[],
        per_user=True,
        per_chat=True,
    )

    dispatcher.add_handler(register_conversation)

    # =========================
    # Error Handler
    # =========================
    def error_handler(update, context):
        """Global xatoliklarni log qiladi."""
        print(f"Update {update} caused error {context.error}")

    dispatcher.add_error_handler(error_handler)

    # =========================
    # Start Polling
    # =========================
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()