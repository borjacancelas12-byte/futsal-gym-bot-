import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Leer token y allowed id desde variables de entorno
TOKEN = os.getenv("8238788823:AAH2Ou1r-QRt-PbofYume0MXCODMrU_MRTE")
if not TOKEN:8238788823:AAH2Ou1r-QRt-PbofYume0MXCODMrU_MRTE
    raise RuntimeError("La variable de entorno TOKEN no está definida. Usa .env para desarrollo o configura la variable en tu host.")

# Permite cambiar el ALLOWED_ID por variable de entorno (si no, usa el valor que pusiste)
ALLOWED_ID = int(os.getenv("ALLOWED_ID", "980036030"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_ID:
        # Para mayor seguridad respondemos y no mostramos nada más
        await update.message.reply_text("⛔ Acceso denegado.")
        return
    await update.message.reply_text(
        "🤖 FutsalGymBot activo.\n"
        "Usa /hoy para tu rutina o /tobillos para movilidad."
    )

async def hoy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_ID:
        return
    texto = (
        "📅 Lunes – Semana 1 – Adaptación\n\n"
        "1. Sentadilla corporal 3×15\n"
        "2. Peso muerto mancuerna 3×10\n"
        "3. Zancadas 3×12/pierna\n"
        "4. Plancha + bird-dog 3×30\"+10\n"
        "5. Salto vertical suave 3×8"
    )
    botones = [
        [InlineKeyboardButton("Sentadilla", url="https://youtu.be/ultWZbUMPL8")],
        [InlineKeyboardButton("Peso muerto", url="https://youtu.be/7KL6xRbZOLc")],
        [InlineKeyboardButton("Zancadas", url="https://youtu.be/3HjJ0qN4pdE")],
        [InlineKeyboardButton("Plancha", url="https://youtu.be/7KSNmFqJj0Y")],
        [InlineKeyboardButton("Salto", url="https://youtu.be/2C-uD_EBiE4")],
    ]
    await update.message.reply_text(texto, reply_markup=InlineKeyboardMarkup(botones))

async def tobillos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_ID:
        return
    texto = (
        "🦶 Rutina diaria tobillos:\n\n"
        "1. Cuclillas profundas 2×30\"\n"
        "2. Elevaciones talones 2×15\n"
        "3. Flexión dorsal banda 2×10/pie\n"
        "4. Círculos tobillo 10×sentido\n"
        "5. Estiramiento gemelos 2×30\"/pierna"
    )
    await update.message.reply_text(texto)

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hoy", hoy))
    app.add_handler(CommandHandler("tobillos", tobillos))
    app.run_polling()
