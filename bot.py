from telegram.ext import ApplicationBuilder, CommandHandler
from handlers import start_command, hoy_command

def create_application(token):
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("hoy", hoy_command))

    return app
