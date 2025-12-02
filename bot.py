# bot.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Función para crear la aplicación del bot
def create_application(token: str):
    application = ApplicationBuilder().token(token).build()

    # Ejemplo de comando /start
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("¡Hola! Soy tu bot.")

    # Añadimos el comando a la aplicación
    application.add_handler(CommandHandler("start", start))

    return application
