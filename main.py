import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging para ver errores y mensajes
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Token del bot
BOT_TOKEN = "Futsalgymbot"

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot de FutsalGym. 😎")

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponibles:\n"
        "/start - iniciar bot\n"
        "/help - ayuda"
    )

async def main():
    # Crear la aplicación del bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Añadir handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Inicializar bot
    await app.initialize()
    await app.start()

    # Configurar puerto dinámico de Render
    PORT = int(os.environ.get("PORT", "8443"))
    APP_NAME = os.environ.get("RENDER_APP_NAME", "<TU_APP>")
    WEBHOOK_URL = f"https://{APP_NAME}.onrender.com/{BOT_TOKEN}"

    # Configurar webhook
    await app.bot.set_webhook(WEBHOOK_URL)
    print(f"Bot funcionando en {WEBHOOK_URL} en el puerto {PORT}")

    # Mantener el bot corriendo
    await app.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


# ----------------------------
# Rutinas completas
# ----------------------------
rutinas = {
    "portero": {
        "futbol": [
            {"ejercicio": "Reacción y reflejos", "youtube": "https://www.youtube.com/watch?v=Y1a4L6V1ZyY"},
            {"ejercicio": "Desplazamientos laterales", "youtube": "https://www.youtube.com/watch?v=2g8S56Oa0jk"},
            {"ejercicio": "Bloqueos y salidas", "youtube": "https://www.youtube.com/watch?v=8bLJk7R5L0A"}
        ],
        "gym": [
            {"ejercicio": "Sentadillas con salto", "youtube": "https://www.youtube.com/watch?v=U3HlEF_E9fo"},
            {"ejercicio": "Plancha lateral", "youtube": "https://www.youtube.com/watch?v=K2VljzCC16g"},
            {"ejercicio": "Flexiones", "youtube": "https://www.youtube.com/watch?v=IODxDxX7oi4"}
        ]
    },
    "ala": {
        "futbol": [
            {"ejercicio": "Regate y control de balón", "youtube": "https://www.youtube.com/watch?v=4rL7QsxY8aU"},
            {"ejercicio": "Pases y cambios de ritmo", "youtube": "https://www.youtube.com/watch?v=3dH3FZsE5hQ"},
            {"ejercicio": "Finalización rápida", "youtube": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        ],
        "gym": [
            {"ejercicio": "Burpees", "youtube": "https://www.youtube.com/watch?v=TU8QYVW0gDU"},
            {"ejercicio": "Zancadas", "youtube": "https://www.youtube.com/watch?v=QOVaHwm-Q6U"},
            {"ejercicio": "Escaladores", "youtube": "https://www.youtube.com/watch?v=nmwgirgXLYM"}
        ]
    },
    "pívot": {
        "futbol": [
            {"ejercicio": "Protección de balón", "youtube": "https://www.youtube.com/watch?v=9m3HfZ5vO9c"},
            {"ejercicio": "Remates de pivote", "youtube": "https://www.youtube.com/watch?v=kFv2p5KytzM"},
            {"ejercicio": "Movimientos de desmarque", "youtube": "https://www.youtube.com/watch?v=8hP9D6kZseM"}
        ],
        "gym": [
            {"ejercicio": "Peso muerto con mancuernas", "youtube": "https://www.youtube.com/watch?v=ytGaGIn3SjE"},
            {"ejercicio": "Press de hombros", "youtube": "https://www.youtube.com/watch?v=B-aVuyhvLHU"},
            {"ejercicio": "Abdominales", "youtube": "https://www.youtube.com/watch?v=1fbU_MkV7NE"}
        ]
    },
    "cierre": {
        "futbol": [
            {"ejercicio": "Marcaje y presión", "youtube": "https://www.youtube.com/watch?v=Hb9Fz7kKkJo"},
            {"ejercicio": "Anticipación de pases", "youtube": "https://www.youtube.com/watch?v=QzB5HIX-KYI"},
            {"ejercicio": "Despejes y coberturas", "youtube": "https://www.youtube.com/watch?v=a3M0Gn1kb1U"}
        ],
        "gym": [
            {"ejercicio": "Sentadillas", "youtube": "https://www.youtube.com/watch?v=aclHkVaku9U"},
            {"ejercicio": "Peso muerto rumano", "youtube": "https://www.youtube.com/watch?v=2SHsk9AzdjA"},
            {"ejercicio": "Plancha frontal", "youtube": "https://www.youtube.com/watch?v=pSHjTRCQxIw"}
        ]
    }
}

# ----------------------------
# Handlers
# ----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy Futsalgymbot 🤖⚽\n"
        "Dime tu posición (portero, ala, pívot, cierre) y te daré la rutina completa de hoy (fútbol + gym)."
    )

async def rutina(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pos = update.message.text.lower()
    if pos in rutinas:
        msg = f"💪 Rutina diaria para *{pos.capitalize()}*:\n\n"
        # Ejercicios de fútbol
        msg += "⚽ *Ejercicios de Fútbol:*\n"
        for e in rutinas[pos]["futbol"]:
            msg += f"- {e['ejercicio']} 🎥 [Video]({e['youtube']})\n"
        # Ejercicios de gym
        msg += "\n🏋️‍♂️ *Ejercicios de Gym:*\n"
        for e in rutinas[pos]["gym"]:
            msg += f"- {e['ejercicio']} 🎥 [Video]({e['youtube']})\n"
        await update.message.reply_markdown(msg)
    else:
        await update.message.reply_text(
            "No reconozco esa posición. Escribe: portero, ala, pívot o cierre."
        )

# ----------------------------
# Agregar handlers a la app
# ----------------------------
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, rutina))

# ----------------------------
# Endpoint para webhook
# ----------------------------
@app.post("/webhook/{token}")
async def webhook(token: str, request: Request):
    if token != TOKEN:
        return {"status": "invalid token"}
    data = await request.json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

# ----------------------------
# Endpoint para test
# ----------------------------
@app.get("/")
def root():
    return {"status": "Futsalgymbot online!"}


