from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

def create_application(token: str):
    app = ApplicationBuilder().token(token).build()

    # Comando /start
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hola! Bot funcionando correctamente.")

    # Comando /help
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Comandos disponibles:\n/start - Iniciar bot\n/help - Ayuda"
        )

    # Agregar handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    return app
