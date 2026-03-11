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
    """

    updater = Updater(settings.TOKEN, use_context=True)
    dp = updater.dispatcher


    # =========================
    # Registration Conversation
    # =========================
    register_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                register_handler,
                pattern="^register:start$"
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
                    pattern="^register:"
                )
            ],
        },
        fallbacks=[],
        per_user=True,
        per_chat=True,
    )

    # Conversation handlerni birinchi qo‘shamiz
    dp.add_handler(register_conversation)


    # =========================
    # Command Handlers
    # =========================
    dp.add_handler(CommandHandler("start", start_bot))
    dp.add_handler(CommandHandler("login", login_page))


    # =========================
    # Inline login tugmasi
    # =========================
    dp.add_handler(
        CallbackQueryHandler(
            login_page,
            pattern="^login_page$"
        )
    )


    # =========================
    # Global Error Handler
    # =========================
    def error_handler(update, context):
        print("ERROR:", context.error)

    dp.add_error_handler(error_handler)


    # =========================
    # Botni ishga tushirish
    # =========================
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()