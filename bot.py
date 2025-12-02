from telegram.ext import ApplicationBuilder, CommandHandler
from handlers import start_command, hoy_command

def create_application(token):8238788823:AAH2Ou1r-QRt-PbofYume0MXCODMrU_MRTE
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("hoy", hoy_command))

    return app
