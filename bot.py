from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers.auth import start, handle_contact, login_command

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("login", login_command))
app.add_handler(MessageHandler(filters.CONTACT, handle_contact))

app.run_polling()