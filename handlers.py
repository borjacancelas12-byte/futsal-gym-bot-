from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler

import os

BOT_TOKEN = os.getenv("Futsalgymbot_token")  # tu token exacto
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, None, workers=0, use_context=True)

app = FastAPI()

# Define un comando /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="¡Hola! Soy Futsalgymbot 🤖")

dp.add_handler(CommandHandler("start", start))

@app.post("/webhook/{token}")
async def webhook(token: str, request: Request):
    if token != BOT_TOKEN:
        return {"status": "invalid token"}
    data = await request.json()
    update = Update.de_json(data, bot)
    dp.process_update(update)
    return {"status": "ok"}
