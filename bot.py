from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# -------- Rutinas según posición de futsal --------
rutinas = {
    "portero": """🔥 *Rutina para Portero*:
- Saltos pliométricos 3x10
- Pecho 4x12
- Hombro 4x10
- Abdomen 4x20
- Trabajo de reflejos""",

    "cierre": """💪 *Rutina para Cierre*:
- Pierna 4x10
- Espalda 4x12
- Core 4x20
- Zancadas 3x12
- Trabajo de agilidad""",

    "ala": """⚡ *Rutina para Ala*:
- HIIT 15 min
- Pierna 3x12
- Pecho 4x12
- Core 4x20
- Trabajo de velocidad""",

    "pivote": """🦵 *Rutina para Pivote*:
- Pierna pesada 5x8
- Glúteo 4x15
- Espalda 4x10
- Trabajo de giro y fuerza"""
}

# Aquí se guardan las posiciones de los usuarios
posiciones_usuarios = {}

# -------- Comandos --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! 👋\n"
        "¿Qué quieres hacer?\n"
        "➡️ Dime tu *posición* (portero, cierre, ala o pivote)\n"
        "➡️ O escribe /hoy para recibir tu rutina de gimnasio 💪"
    )

async def hoy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in posiciones_usuarios:
        await update.message.reply_text(
            "No sé tu posición 🤔\n"
            "Dime si eres portero, cierre, ala o pivote."
        )
        return

    posicion = posiciones_usuarios[user_id]
    rutina = rutinas[posicion]

    await update.message.reply_text(rutina, parse_mode="Markdown")

async def guardar_posicion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower().strip()

    if texto in rutinas:
        posiciones_usuarios[update.message.from_user.id] = texto
        await update.message.reply_text(
            f"Perfecto, guardaré que eres *{texto}* 📝.\n"
            "Ahora escribe /hoy para recibir tu rutina 🔥",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "No reconozco esa posición 😅\n"
            "Usa una de estas: portero, cierre, ala, pivote."
        )

# -------- Iniciar el bot --------

async def main():
    app = Application.builder().token("8238788823:AAH2Ou1r-QRt-PbofYume0MXCODMrU_MRTE").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hoy", hoy))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guardar_posicion))

    print("🤖 Bot iniciado...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
