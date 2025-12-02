# main.py
import os
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import random

TOKEN = os.getenv("Futsalgymbot_token")
bot = Bot(token=TOKEN)
app = FastAPI()

# Crear aplicación de Telegram
application = ApplicationBuilder().token(TOKEN).build()

# Rutinas de ejemplo
rutinas = {
    "portero": [
        {
            "ejercicio": "Reacción y reflejos",
            "youtube": "https://www.youtube.com/watch?v=Y1a4L6V1ZyY"
        },
        {
            "ejercicio": "Desplazamientos laterales",
            "youtube": "https://www.youtube.com/watch?v=2g8S56Oa0jk"
        },
    ],
    "ala": [
        {
            "ejercicio": "Regate y control de balón",
            "youtube": "https://www.youtube.com/watch?v=4rL7QsxY8aU"
        },
        {
            "ejercicio": "Pases y cambios de ritmo",
            "youtube": "https://www.youtube.com/watch?v=3dH3FZsE5hQ"
        },
    ],
    "pívot": [
        {
            "ejercicio": "Finalización y remates",
            "youtube": "https://www.youtube.com/watch?v=kFv2p5KytzM"
        },
        {
            "ejercicio": "Protección de balón",
            "youtube": "https://www.youtube.com/watch?v=9m3HfZ5vO9c"
        },
    ],
    "cierre": [
        {
            "ejercicio": "Defensa y anticipación",
            "youtube": "https://www.youtube.com/watch?v=Jk6w9F0iHhE"
        },
        {
            "ejercicio": "Marcaje y presión",
            "youtube": "https://www.youtube.com/watch?v=Hb9Fz7kKkJo"
        },
    ],
}

# Handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy Futsalgymbot 🤖⚽\n"
        "Dime tu posición (portero, ala, pívot, cierre) y te daré la rutina de hoy."
    )

# Handler de mensajes de texto
async def rutina(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()
    if msg in rutinas:
        rutina = random.choice(rutinas[msg])
        await update.message.reply_text(
            f"💪 Ejercicio: {rutina['ejercicio']}\n"
            f"🎥 Video de ejemplo: {rutina['youtube']}"
        )
    else:
        await update.message.reply_text(
            "No reconozco esa posición. Por favor escribe: portero, ala, pívot o cierre."
        )

# Agregar handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, rutina))

# Endpoint de webhook
@app.post("/webhook/{token}")
async def webhook(token: str, request: Request):
    if token != TOKEN:
        return {"status": "invalid token"}
    data = await request.json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

# Endpoint para probar que el servidor está online
@app.get("/")
def root():
    return {"status": "Futsalgymbot online!"}

