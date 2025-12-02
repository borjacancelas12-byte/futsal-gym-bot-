from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

def create_application(token: str):
    app = ApplicationBuilder().token(token).build()

    # Comando de ejemplo
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hola! Bot funcionando correctamente.")

    app.add_handler(CommandHandler("start", start))
    return app
