# main.py
import os
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("Futsalgymbot_token")
bot = Bot(token=TOKEN)
app = FastAPI()

# Creamos la aplicación de Telegram
application = ApplicationBuilder().token(TOKEN).build()

# Handler de /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy Futsalgymbot. Escríbeme tu posición y te daré la rutina de hoy."
    )

application.add_handler(CommandHandler("start", start))

# Endpoint de webhook
@app.post("/webhook/{token}")
async def webhook(token: str, request: Request):
    if token != TOKEN:
        return {"status": "invalid token"}
    data = await request.json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

# Test básico de que el servidor corre
@app.get("/")
def root():
    return {"status": "Futsalgymbot online!"}

